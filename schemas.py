from pydantic import BaseModel
from typing import List, Optional

class ImageRequest(BaseModel):
    product_name: str
    input_image_urls: List[str]

class ImageRequestCreate(BaseModel):
    product_name: str
    input_image_urls: str

class ImageRequestStatus(BaseModel):
    request_id: str
    status: str
    output_image_urls: Optional[str] = None
