from pydantic import BaseModel
from typing import Optional
from datetime import date

class ReceiveProductBase(BaseModel):
    product_id: int
    quantity: float
    unit_price: float
    sub_total: float
    supplier_id: int
    received_date: date
    user_id: int
    purchase_order_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": 1,
                "quantity": 100.0,
                "unit_price": 5.99,
                "sub_total": 599.00,
                "supplier_id": 1,
                "received_date": "2023-05-20",
                "user_id": 1,
                "purchase_order_id": 1
            }
        }

class ReceiveProductCreate(ReceiveProductBase):
    receive_product_id: Optional[int] = None  # Optional for creation, will be set by the database
    pass

class ReceiveProductResponse(ReceiveProductBase):
    receive_product_id: int
    

    class Config:
        from_attributes = True

class ReceiveProductUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    sub_total: Optional[float] = None
    supplier_id: Optional[int] = None
    received_date: Optional[date] = None
    user_id: Optional[int] = None
    purchase_order_id: Optional[int] = None