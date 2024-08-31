import uuid
from PIL import Image
from io import BytesIO
import requests

def generate_request_id():
    return str(uuid.uuid4())

def compress_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=50)
    buffer.seek(0)

    return buffer
