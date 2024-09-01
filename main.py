from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from .models import ImageProcessingRequest
from .schemas import ImageRequestCreate, ImageRequestStatus
from .utils import generate_request_id
from .celery_worker import process_images

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/upload", response_model=ImageRequestStatus)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    csv_data = content.decode('utf-8').splitlines()

    # Parse CSV data here
    for row in csv_data:
        data = row.split(',')
        request_id = generate_request_id()
        
        image_request = ImageProcessingRequest(
            product_name=data[1],
            input_image_urls=','.join(data[2:]),
            request_id=request_id,
        )

        db.add(image_request)
        db.commit()
        db.refresh(image_request)

        process_images.delay(request_id)

        return {"request_id": request_id, "status": "processing"}

@app.get("/status/{request_id}", response_model=ImageRequestStatus)
def check_status(request_id: str, db: Session = Depends(get_db)):
    request = db.query(ImageProcessingRequest).filter_by(request_id=request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request ID not found")

    return {
        "request_id": request.request_id,
        "status": request.status,
        "output_image_urls": request.output_image_urls,
    }
