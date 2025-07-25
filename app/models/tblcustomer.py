from pydantic import BaseModel
from typing import Optional

class CustomerBase(BaseModel):
    customer_code: str
    customer_name: str
    contact: str
    address: str

    class Config:
        json_schema_extra = {
            "example": {
                "customer_code": "CUST-001",
                "customer_name": "John Doe",
                "contact": "1234567890",
                "address": "123 Main St, City"
            }
        }

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: int

    class Config:
        from_attributes = True

class CustomerUpdate(BaseModel):
    customer_code: Optional[str] = None
    customer_name: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None