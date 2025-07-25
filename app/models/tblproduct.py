from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    produce_code: str
    product_name: str
    unit_id: int
    category_id: int
    unit_in_stock: float
    unit_price: float
    discount_percentage: float = 0.0
    reorder_level: float
    user_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "produce_code": "string",
                "product_name": "string",
                "unit_id": 0,
                "category_id": 0,
                "unit_in_stock": 0,
                "unit_price": 0,
                "discount_percentage": 0,
                "reorder_level": 0,
                "user_id": 0
            }
        }

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: int

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    produce_code: Optional[str] = None
    product_name: Optional[str] = None
    unit_id: Optional[int] = None
    category_id: Optional[int] = None
    unit_in_stock: Optional[float] = None
    unit_price: Optional[float] = None
    discount_percentage: Optional[float] = None
    reorder_level: Optional[float] = None
    user_id: Optional[int] = None