from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tblproductunit import ProductUnitCreate, ProductUnitResponse
from typing import List
import mysql.connector

router= APIRouter(prefix="/product-unit", tags=["Product Unit"])
@router.get("/", response_model=List[ProductUnitResponse])
def get_product_units():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT unit_id, unit_name FROM tblproductunit")
        units = cursor.fetchall()
        return [ProductUnitResponse(**unit) for unit in units]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{unit_id}", response_model=ProductUnitResponse)
def get_product_unit(unit_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT unit_id, unit_name FROM tblproductunit WHERE unit_id = %s", (unit_id,))
        unit = cursor.fetchone()
        if not unit:
            raise HTTPException(status_code=404, detail="Product unit not found")
        return ProductUnitResponse(**unit)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=ProductUnitResponse, status_code=status.HTTP_201_CREATED)
def create_product_unit(unit: ProductUnitCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # First check if unit with same name already exists
        cursor.execute(
            "SELECT unit_id FROM tblproductunit WHERE unit_name = %s", 
            (unit.unit_name,)
        )
        existing_unit = cursor.fetchone()
        
        if existing_unit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unit with this name already exists"
            )
        
        # Insert new unit if name is unique
        cursor.execute(
            "INSERT INTO tblproductunit (unit_name) VALUES (%s)", 
            (unit.unit_name,)
        )
        conn.commit()
        
        # Get the ID of the newly created unit
        unit_id = cursor.lastrowid
        return ProductUnitResponse(unit_id=unit_id, **unit.dict())
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.put("/{unit_id}", response_model=ProductUnitResponse)
def update_product_unit(unit_id: int, unit: ProductUnitCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if the unit exists
        cursor.execute("SELECT unit_id FROM tblproductunit WHERE unit_id = %s", (unit_id,))
        existing_unit = cursor.fetchone()
        
        if not existing_unit:
            raise HTTPException(status_code=404, detail="Product unit not found")
        
        # Update the unit
        cursor.execute(
            "UPDATE tblproductunit SET unit_name = %s WHERE unit_id = %s", 
            (unit.unit_name, unit_id)
        )
        conn.commit()
        
        return ProductUnitResponse(unit_id=unit_id, **unit.dict())
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{unit_id}", status_code=status.HTTP_200_OK)
def delete_product_unit(unit_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if the unit exists
        cursor.execute("SELECT unit_id FROM tblproductunit WHERE unit_id = %s", (unit_id,))
        existing_unit = cursor.fetchone()
        
        if not existing_unit:
            raise HTTPException(
                status_code=404, 
                detail=f"Product unit with ID {unit_id} not found"
            )
        
        # Delete the unit
        cursor.execute("DELETE FROM tblproductunit WHERE unit_id = %s", (unit_id,))
        conn.commit()
        
        return {"detail": f"Product unit with ID {unit_id} deleted successfully"}
    
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, 
            detail=f"Database error: {err}"
        )
    
    finally:
        cursor.close()
        conn.close()
