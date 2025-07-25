from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import IntEnum

class PaymentType(IntEnum):
    CASH = 1
    CREDIT = 2
    BANK_TRANSFER = 3
    MOBILE_MONEY = 4

class InvoiceBase(BaseModel):
    customer_id: int
    payment_type: PaymentType
    total_amount: float
    amount_tendered: float
    bank_account_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    date_recorded: date
    user_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "payment_type": 1,
                "total_amount": 100.50,
                "amount_tendered": 120.00,
                "bank_account_name": "My Business",
                "bank_account_number": "1234567890",
                "date_recorded": "2023-05-15",
                "user_id": 1
            }
        }

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    invoice_id: int

    class Config:
        from_attributes = True

class InvoiceUpdate(BaseModel):
    customer_id: Optional[int] = None
    payment_type: Optional[PaymentType] = None
    total_amount: Optional[float] = None
    amount_tendered: Optional[float] = None
    bank_account_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    date_recorded: Optional[date] = None
    user_id: Optional[int] = None