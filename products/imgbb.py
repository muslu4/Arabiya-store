import requests
from django.conf import settings

IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"

class ImgBBError(Exception):
    pass

def upload_image_file(file_obj, name_prefix="upload"):
    """
    Upload a file-like object to ImgBB and return the direct image URL.
    - file_obj: InMemoryUploadedFile or file-like
    - returns: str URL
    """
    api_key = settings.IMGBB_API_KEY
    if not api_key:
        raise ImgBBError("IMGBB_API_KEY is not set")

    files = {"image": file_obj.read()}
    data = {"key": api_key, "name": name_prefix}

    resp = requests.post(IMGBB_UPLOAD_URL, data=data, files=files, timeout=30)
    if resp.status_code != 200:
        raise ImgBBError(f"Upload failed: {resp.status_code} - {resp.text}")

    payload = resp.json()
    if not payload.get("success"):
        raise ImgBBError(f"Upload not successful: {payload}")

    # Prefer display_url or url
    data = payload.get("data", {})
    return data.get("url") or data.get("display_url")