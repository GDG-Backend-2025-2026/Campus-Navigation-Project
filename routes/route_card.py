from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
import uuid

# Define Blueprint
route_card_bp = Blueprint('route_cards', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg', 'image/webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Magic byte signatures for supported image formats
IMAGE_SIGNATURES = {
    b'\x89PNG\r\n\x1a\n': 'png',       # PNG
    b'\xff\xd8\xff': 'jpeg',            # JPEG
    b'RIFF': 'webp',                    # WebP (check RIFF + WEBP)
}


def validate_image(file_stream):
    """
    Validate that the uploaded file is actually an image by reading its
    magic bytes. Works on Python 3.13+ (no imghdr dependency).
    Returns the detected image type or None if invalid.
    """
    header = file_stream.read(12)
    file_stream.seek(0)

    if len(header) < 4:
        return None

    # PNG: starts with 8-byte signature
    if header[:8] == b'\x89PNG\r\n\x1a\n':
        return 'png'

    # JPEG: starts with FF D8 FF
    if header[:3] == b'\xff\xd8\xff':
        return 'jpeg'

    # WebP: starts with RIFF....WEBP
    if header[:4] == b'RIFF' and header[8:12] == b'WEBP':
        return 'webp'

    return None


@route_card_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_route_image():
    """
    Upload a route card image.
    ---
    tags:
      - Route Cards
    consumes:
      - multipart/form-data
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: "Bearer <JWT token>"
      - in: formData
        name: file
        type: file
        required: true
        description: "Image file (PNG, JPG, JPEG, or WebP). Max 5 MB."
    responses:
      200:
        description: File uploaded successfully
        schema:
          type: object
          properties:
            message:
              type: string
            url:
              type: string
              description: Publicly accessible URL of the uploaded image
      400:
        description: Bad request — no file, empty filename, or disallowed type
      401:
        description: Unauthorized — missing or invalid JWT token
      413:
        description: File too large (exceeds 5 MB)
    """

    # --- Check file part exists ---
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # --- Check filename is not empty ---
    if not file.filename or file.filename.strip() == '':
        return jsonify({'error': 'No file selected'}), 400

    # --- Check extension ---
    if not allowed_file(file.filename):
        return jsonify({
            'error': 'File type not allowed. Accepted: png, jpg, jpeg, webp'
        }), 400

    # --- Check MIME type ---
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        return jsonify({
            'error': f'Invalid MIME type: {file.content_type}. '
                     f'Accepted: {", ".join(ALLOWED_MIME_TYPES)}'
        }), 400

    # --- Validate actual image content (magic bytes) ---
    if not validate_image(file.stream):
        return jsonify({
            'error': 'File content does not match a valid image format'
        }), 400

    # --- Explicit size check (belt-and-suspenders with MAX_CONTENT_LENGTH) ---
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > MAX_FILE_SIZE:
        return jsonify({
            'error': f'File size ({size} bytes) exceeds the 5 MB limit'
        }), 413

    # --- Build unique filename and save ---
    original = secure_filename(file.filename)
    ext = original.rsplit('.', 1)[1].lower() if '.' in original else 'png'
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)

    # --- Construct readable URL ---
    file_url = f"{request.host_url}static/uploads/{unique_filename}"

    return jsonify({
        'message': 'File uploaded successfully',
        'url': file_url
    }), 200
