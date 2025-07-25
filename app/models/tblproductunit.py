from pydantic import BaseModel
from typing import Optional

# Request model for creating/updating units
class ProductUnitCreate(BaseModel):
    unit_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "unit_name": "kg"
            }
        }

# Response model (includes the ID)
class ProductUnitResponse(ProductUnitCreate):
    unit_id: int

    class Config:
        from_attributes = True