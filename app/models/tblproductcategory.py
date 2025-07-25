from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class ProductCategoryCreate(BaseModel):
    category_name: str

# Response model (includes the ID)
class ProductCategoryResponse(ProductCategoryCreate):
    category_id: int

    class Config:
        from_attributes = True
