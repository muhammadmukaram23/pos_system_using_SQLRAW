from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tblsupplier import SupplierCreate, SupplierResponse, SupplierUpdate
from typing import List
import mysql.connector
router = APIRouter(prefix="/supplier", tags=["Supplier"])


@router.get("/", response_model=List[SupplierResponse])
def get_suppliers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT supplier_id, supplier_code, supplier_name, supplier_contact, supplier_address FROM tblsupplier")
        suppliers = cursor.fetchall()
        return [SupplierResponse(**supplier) for supplier in suppliers]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM tblsupplier WHERE supplier_id = %s", (supplier_id,))
        supplier = cursor.fetchone()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return SupplierResponse(**supplier)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: SupplierCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if supplier_code is unique
        cursor.execute("SELECT supplier_id FROM tblsupplier WHERE supplier_code = %s", (supplier.supplier_code,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Supplier with this code already exists"
            )
        
        # Insert new supplier
        cursor.execute("""
            INSERT INTO tblsupplier (supplier_code, supplier_name, supplier_contact, 
                                     supplier_address, supplier_email, contact_person, 
                                     bank_account_name, bank_account_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            supplier.supplier_code,
            supplier.supplier_name,
            supplier.supplier_contact,
            supplier.supplier_address,
            supplier.supplier_email,
            supplier.contact_person,
            supplier.bank_account_name,
            supplier.bank_account_number
        ))
        conn.commit()
        
        # Get the newly created supplier ID
        supplier_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tblsupplier WHERE supplier_id = %s", (supplier_id,))
        new_supplier = cursor.fetchone()
        return SupplierResponse(**new_supplier)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: int, supplier: SupplierUpdate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if supplier exists
        cursor.execute("SELECT supplier_id FROM tblsupplier WHERE supplier_id = %s", (supplier_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Supplier not found")
        
        # Prepare update query
        update_fields = [f"{field} = %s" for field, value in supplier.dict().items() if value is not None]
        update_values = [value for value in supplier.dict().values() if value is not None]
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_query = f"UPDATE tblsupplier SET {', '.join(update_fields)} WHERE supplier_id = %s"
        update_values.append(supplier_id)
        
        cursor.execute(update_query, tuple(update_values))
        conn.commit()
        
        # Fetch updated supplier
        cursor.execute("SELECT * FROM tblsupplier WHERE supplier_id = %s", (supplier_id,))
        updated_supplier = cursor.fetchone()
        
        return SupplierResponse(**updated_supplier)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{supplier_id}", status_code=status.HTTP_200_OK)
def delete_supplier(supplier_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if supplier exists
        cursor.execute("SELECT supplier_id FROM tblsupplier WHERE supplier_id = %s", (supplier_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Supplier not found")
        
        # Delete supplier
        cursor.execute("DELETE FROM tblsupplier WHERE supplier_id = %s", (supplier_id,))
        conn.commit()
        
        return {"detail": "Supplier deleted successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
