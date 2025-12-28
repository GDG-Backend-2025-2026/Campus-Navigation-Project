import cloudinary
import cloudinary.uploader
from flask import current_app


def init_cloudinary():
    """Initialize Cloudinary with config from Flask app."""
    cloudinary.config(
        cloud_name=current_app.config.get('CLOUDINARY_CLOUD_NAME'),
        api_key=current_app.config.get('CLOUDINARY_API_KEY'),
        api_secret=current_app.config.get('CLOUDINARY_API_SECRET'),
        secure=True
    )


def upload_image(file, folder="campus-navigation"):
    """
    Upload an image to Cloudinary.
    
    Args:
        file: File object or file path to upload
        folder: Cloudinary folder to upload to
        
    Returns:
        dict with 'success' and 'url' or 'error' keys
    """
    try:
        init_cloudinary()
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="image"
        )
        return {
            'success': True,
            'url': result.get('secure_url'),
            'public_id': result.get('public_id')
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def delete_image(public_id):
    """
    Delete an image from Cloudinary.
    
    Args:
        public_id: The public ID of the image to delete
        
    Returns:
        dict with 'success' key
    """
    try:
        init_cloudinary()
        result = cloudinary.uploader.destroy(public_id)
        return {
            'success': result.get('result') == 'ok'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

