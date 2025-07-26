from pydantic import BaseModel
from typing import Optional
from datetime import date

class PurchaseOrderBase(BaseModel):
    product_id: int
    quantity: float
    unit_price: float
    sub_total: float
    supplier_id: int
    order_date: date
    user_id: int
    status: str = "pending"  # Default value matches your table

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": 1,
                "quantity": 100.0,
                "unit_price": 5.99,
                "sub_total": 599.00,
                "supplier_id": 1,
                "order_date": "2023-05-20",
                "user_id": 1,
                "status": "pending"
            }
        }

class PurchaseOrderCreate(PurchaseOrderBase):
    purchase_order_id: Optional[int] = None  # Will be set by database
    pass

class PurchaseOrderResponse(PurchaseOrderBase):
    purchase_order_id: int
    
    class Config:
        from_attributes = True  # Orm_mode in older Pydantic versions

class PurchaseOrderUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    sub_total: Optional[float] = None
    supplier_id: Optional[int] = None
    order_date: Optional[date] = None
    user_id: Optional[int] = None
    status: Optional[str] = None