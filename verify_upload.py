"""
Verification script for the Route Card Image Upload endpoint.

Tests all scenarios:
  1. Successful upload of a valid PNG image
  2. Rejected when no file is provided
  3. Rejected for disallowed file type
  4. Rejected without JWT token (401)
  5. Returned URL is accessible

Usage:
  1. Start the dev server: python app.py
  2. In another terminal:  python verify_upload.py
"""
import requests
import struct
import os
import sys

from app import create_app
from flask_jwt_extended import create_access_token

BASE_URL = 'http://127.0.0.1:5000'
UPLOAD_URL = f'{BASE_URL}/api/route-cards/upload'

results = []


def log(test_name, passed, detail=''):
    status = '✅ PASS' if passed else '❌ FAIL'
    results.append(passed)
    print(f"  {status} — {test_name}" + (f"  ({detail})" if detail else ''))


def create_valid_png(path):
    """Create a minimal valid 1x1 red PNG file."""
    import zlib

    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack('>I', len(data)) + c + crc

    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)  # 1x1, 8-bit RGB
    raw_row = b'\x00\xff\x00\x00'  # filter byte + red pixel
    idat_data = zlib.compress(raw_row)

    with open(path, 'wb') as f:
        f.write(signature)
        f.write(chunk(b'IHDR', ihdr_data))
        f.write(chunk(b'IDAT', idat_data))
        f.write(chunk(b'IEND', b''))


def get_token():
    """Generate a valid JWT token using the app context."""
    app = create_app()
    with app.app_context():
        return create_access_token(identity='test_admin')


def main():
    print('\n=== Route Card Upload Endpoint Tests ===\n')

    token = get_token()
    auth_headers = {'Authorization': f'Bearer {token}'}

    # --- Create test files ---
    create_valid_png('test_valid.png')
    with open('test_bad.txt', 'w') as f:
        f.write('not an image')

    try:
        # 1. Successful upload
        with open('test_valid.png', 'rb') as img:
            r = requests.post(UPLOAD_URL, headers=auth_headers, files={'file': ('test.png', img, 'image/png')})
        log('Valid image upload', r.status_code == 200, f'status={r.status_code}')
        uploaded_url = r.json().get('url', '') if r.status_code == 200 else ''

        # 2. No file part
        r = requests.post(UPLOAD_URL, headers=auth_headers)
        log('Reject when no file part', r.status_code == 400, f'status={r.status_code}')

        # 3. Disallowed file type
        with open('test_bad.txt', 'rb') as f:
            r = requests.post(UPLOAD_URL, headers=auth_headers, files={'file': ('bad.txt', f, 'text/plain')})
        log('Reject disallowed file type', r.status_code == 400, f'status={r.status_code}')

        # 4. No JWT token (401)
        with open('test_valid.png', 'rb') as img:
            r = requests.post(UPLOAD_URL, files={'file': ('test.png', img, 'image/png')})
        log('Reject without JWT', r.status_code == 401, f'status={r.status_code}')

        # 5. Uploaded URL is accessible
        if uploaded_url:
            r = requests.get(uploaded_url)
            log('Uploaded image URL accessible', r.status_code == 200, f'url={uploaded_url}')
        else:
            log('Uploaded image URL accessible', False, 'no URL from test 1')

    finally:
        # Cleanup temp files
        for f in ('test_valid.png', 'test_bad.txt'):
            if os.path.exists(f):
                os.remove(f)

    # --- Summary ---
    passed = sum(results)
    total = len(results)
    print(f'\n=== Results: {passed}/{total} passed ===\n')
    sys.exit(0 if passed == total else 1)


if __name__ == '__main__':
    main()
