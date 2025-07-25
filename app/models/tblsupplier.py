from pydantic import BaseModel, EmailStr
from typing import Optional

class SupplierBase(BaseModel):
    supplier_code: str
    supplier_name: str
    supplier_contact: str
    supplier_address: str
    supplier_email: Optional[EmailStr] = None
    contact_person: Optional[str] = None
    bank_account_name: Optional[str] = None
    bank_account_number: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "supplier_code": "SUPP-001",
                "supplier_name": "ABC Distributors",
                "supplier_contact": "1234567890",
                "supplier_address": "123 Industrial Zone",
                "supplier_email": "contact@abcdist.com",
                "contact_person": "John Smith",
                "bank_account_name": "ABC Distributors",
                "bank_account_number": "1234567890123"
            }
        }

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    supplier_id: int

    class Config:
        from_attributes = True

class SupplierUpdate(BaseModel):
    supplier_code: Optional[str] = None
    supplier_name: Optional[str] = None
    supplier_contact: Optional[str] = None
    supplier_address: Optional[str] = None
    supplier_email: Optional[EmailStr] = None
    contact_person: Optional[str] = None
    bank_account_name: Optional[str] = None
    bank_account_number: Optional[str] = None