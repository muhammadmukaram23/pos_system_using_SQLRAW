from pydantic import BaseModel
from typing import Optional

class SaleBase(BaseModel):
    invoice_id: int
    product_id: int
    quantity: float
    unit_price: float
    sub_total: float

    class Config:
        json_schema_extra = {
            "example": {
                "invoice_id": 1,
                "product_id": 1,
                "quantity": 2.0,
                "unit_price": 10.99,
                "sub_total": 21.98
            }
        }

class SaleCreate(SaleBase):
    sales_id: Optional[int] = None  # Optional for creation, will be set by the database
    pass

class SaleResponse(SaleBase):
    sales_id: int

    class Config:
        from_attributes = True

class SaleUpdate(BaseModel):
    invoice_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    sub_total: Optional[float] = None