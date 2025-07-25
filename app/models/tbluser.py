from pydantic import BaseModel
from typing import Optional
from enum import IntEnum

class DesignationType(IntEnum):
    STAFF = 1
    MANAGER = 2
    ADMIN = 3

class AccountType(IntEnum):
    REGULAR = 1
    ADMIN = 2
    SUPER_ADMIN = 3

class UserBase(BaseModel):
    username: str
    fullname: str
    designation: DesignationType
    contact: str
    account_type: AccountType

class UserCreate(UserBase):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "secure123",
                "fullname": "John Doe",
                "designation": 1,
                "contact": "1234567890",
                "account_type": 1
            }
        }

class UserResponse(UserBase):
    user_id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    designation: Optional[DesignationType] = None
    contact: Optional[str] = None
    account_type: Optional[AccountType] = None
    password: Optional[str] = None