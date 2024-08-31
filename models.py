from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class ImageProcessingRequest(Base):
    __tablename__ = "image_processing_requests"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    input_image_urls = Column(String)
    output_image_urls = Column(String, nullable=True)
    status = Column(String, default="pending")
    request_id = Column(String, unique=True, index=True)
