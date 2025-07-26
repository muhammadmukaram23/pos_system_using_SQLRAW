from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tblreceiveproduct import ReceiveProductCreate, ReceiveProductResponse, ReceiveProductUpdate
from app.models.tblsupplier import SupplierResponse
from app.models.tblproduct import ProductResponse
from app.models.tbluser import UserResponse
from typing import List
import mysql.connector
router = APIRouter(prefix="/receive-product", tags=["Receive Product"])

@router.get("/", response_model=List[ReceiveProductResponse])
def get_receive_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
             SELECT rp.receive_product_id, rp.product_id, 
           rp.quantity, rp.unit_price, rp.sub_total, 
           rp.supplier_id, rp.received_date, 
           rp.user_id, rp.purchase_order_id,
           s.supplier_name AS supplier_name,
           p.product_name AS product_name,
           u.username AS received_by
    FROM tblreceiveproduct rp
    JOIN tblsupplier s ON rp.supplier_id = s.supplier_id
    JOIN tblproduct p ON rp.product_id = p.product_id
    JOIN tbluser u ON rp.user_id = u.user_id
        """)

  
        receive_products = cursor.fetchall()
        return [ReceiveProductResponse(**rp) for rp in receive_products]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=ReceiveProductResponse, status_code=status.HTTP_201_CREATED)
def create_receive_product(receive_product: ReceiveProductCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            INSERT INTO tblreceiveproduct (product_id, quantity, 
                                           unit_price, sub_total, 
                                           supplier_id, received_date, 
                                           user_id, purchase_order_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            receive_product.product_id,
            receive_product.quantity,
            receive_product.unit_price,
            receive_product.sub_total,
            receive_product.supplier_id,
            receive_product.received_date,
            receive_product.user_id,
            receive_product.purchase_order_id
        ))
        conn.commit()
        receive_product_id = cursor.lastrowid
        
        # Fetch the newly created receive product
        cursor.execute("SELECT * FROM tblreceiveproduct WHERE receive_product_id = %s", (receive_product_id,))
        new_receive_product = cursor.fetchone()
        return ReceiveProductResponse(**new_receive_product)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.put("/{receive_product_id}", response_model=ReceiveProductResponse)
def update_receive_product(receive_product_id: int, receive_product: ReceiveProductUpdate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if receive product exists
        cursor.execute("SELECT receive_product_id FROM tblreceiveproduct WHERE receive_product_id = %s", (receive_product_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Receive Product not found")
        
        # Update the receive product
        cursor.execute("""
            UPDATE tblreceiveproduct 
            SET product_id = %s, quantity = %s, unit_price = %s, 
                sub_total = %s, supplier_id = %s, received_date = %s, 
                user_id = %s, purchase_order_id = %s
            WHERE receive_product_id = %s
        """, (
            receive_product.product_id,
            receive_product.quantity,
            receive_product.unit_price,
            receive_product.sub_total,
            receive_product.supplier_id,
            receive_product.received_date,
            receive_product.user_id,
            receive_product.purchase_order_id,
            receive_product_id
        ))
        conn.commit()
        
        # Fetch the updated receive product
        cursor.execute("SELECT * FROM tblreceiveproduct WHERE receive_product_id = %s", (receive_product_id,))
        updated_receive_product = cursor.fetchone()
        return ReceiveProductResponse(**updated_receive_product)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{receive_product_id}", status_code=status.HTTP_200_OK)
def delete_receive_product(receive_product_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if receive product exists
        cursor.execute("SELECT receive_product_id FROM tblreceiveproduct WHERE receive_product_id = %s", (receive_product_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Receive Product not found")
        
        # Delete the receive product
        cursor.execute("DELETE FROM tblreceiveproduct WHERE receive_product_id = %s", (receive_product_id,))
        conn.commit()
        
        return {"status": "success", "message": "Receive Product deleted successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{receive_product_id}", response_model=ReceiveProductResponse)
def get_receive_product(receive_product_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if receive product exists
        cursor.execute("SELECT * FROM tblreceiveproduct WHERE receive_product_id = %s", (receive_product_id,))
        receive_product = cursor.fetchone()
        if not receive_product:
            raise HTTPException(status_code=404, detail="Receive Product not found")
        
        return ReceiveProductResponse(**receive_product)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()