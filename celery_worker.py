from celery import Celery
from .utils import compress_image
from .database import SessionLocal
from .models import ImageProcessingRequest
import os

celery = Celery(__name__, broker='redis://localhost:6379/0')

@celery.task
def process_images(request_id):
    db = SessionLocal()
    request = db.query(ImageProcessingRequest).filter_by(request_id=request_id).first()

    input_urls = request.input_image_urls.split(',')
    output_urls = []

    for url in input_urls:
        compressed_image = compress_image(url)
        output_url = upload_compressed_image(compressed_image)  # Define your upload logic
        output_urls.append(output_url)

    request.output_image_urls = ','.join(output_urls)
    request.status = 'completed'
    db.commit()
    db.close()
