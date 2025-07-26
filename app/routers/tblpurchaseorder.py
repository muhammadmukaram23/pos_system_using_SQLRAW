from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tblpurchaseorder import PurchaseOrderCreate, PurchaseOrderResponse, PurchaseOrderUpdate
from app.models.tblproduct import ProductResponse
from app.models.tblsupplier import SupplierResponse
from app.models.tbluser import UserResponse
from typing import List
import mysql.connector

router = APIRouter(prefix="/purchase-order", tags=["Purchase Order"])

@router.get("/", response_model=List[PurchaseOrderResponse])
def get_purchase_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT po.purchase_order_id, po.supplier_id, po.product_id, 
                   po.quantity, po.unit_price, po.sub_total, 
                   po.order_date, po.user_id,
                   s.supplier_name AS supplier_name,
                   p.product_name AS product_name,
                   u.username AS ordered_by
            FROM tblpurchaseorder po
            JOIN tblsupplier s ON po.supplier_id = s.supplier_id
            JOIN tblproduct p ON po.product_id = p.product_id
            JOIN tbluser u ON po.user_id = u.user_id
        """)
        purchase_orders = cursor.fetchall()
        return [PurchaseOrderResponse(**po) for po in purchase_orders]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
def create_purchase_order(purchase_order: PurchaseOrderCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            INSERT INTO tblpurchaseorder (supplier_id, product_id, 
                                          quantity, unit_price, 
                                          sub_total, order_date, 
                                          user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            purchase_order.supplier_id,
            purchase_order.product_id,
            purchase_order.quantity,
            purchase_order.unit_price,
            purchase_order.sub_total,
            purchase_order.order_date,
            purchase_order.user_id
        ))
        conn.commit()
        
        # Fetch the newly created purchase order
        cursor.execute("SELECT * FROM tblpurchaseorder WHERE purchase_order_id = %s", (cursor.lastrowid,))
        new_purchase_order = cursor.fetchone()
        return PurchaseOrderResponse(**new_purchase_order)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()


@router.put("/{purchase_order_id}", response_model=PurchaseOrderResponse)
def update_purchase_order(purchase_order_id: int, purchase_order: PurchaseOrderUpdate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if purchase order exists
        cursor.execute("SELECT purchase_order_id FROM tblpurchaseorder WHERE purchase_order_id = %s", (purchase_order_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Purchase Order not found")
        
        cursor.execute("""
            UPDATE tblpurchaseorder 
            SET supplier_id = %s, product_id = %s, 
                quantity = %s, unit_price = %s, 
                sub_total = %s, order_date = %s, 
                user_id = %s
            WHERE purchase_order_id = %s
        """, (
            purchase_order.supplier_id,
            purchase_order.product_id,
            purchase_order.quantity,
            purchase_order.unit_price,
            purchase_order.sub_total,
            purchase_order.order_date,
            purchase_order.user_id,
            purchase_order_id
        ))
        conn.commit()
        
        # Fetch the updated purchase order
        cursor.execute("SELECT * FROM tblpurchaseorder WHERE purchase_order_id = %s", (purchase_order_id,))
        updated_purchase_order = cursor.fetchone()
        return PurchaseOrderResponse(**updated_purchase_order)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()


@router.delete("/{purchase_order_id}", status_code=status.HTTP_200_OK)
def delete_purchase_order(purchase_order_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if purchase order exists
        cursor.execute("SELECT purchase_order_id FROM tblpurchaseorder WHERE purchase_order_id = %s", (purchase_order_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Purchase Order not found")
        
        # Delete the purchase order
        cursor.execute("DELETE FROM tblpurchaseorder WHERE purchase_order_id = %s", (purchase_order_id,))
        conn.commit()
        
        return {"detail": "Purchase Order deleted successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{purchase_order_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(purchase_order_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT po.purchase_order_id, po.supplier_id, po.product_id, 
                   po.quantity, po.unit_price, po.sub_total, 
                   po.order_date, po.user_id,
                   s.supplier_name AS supplier_name,
                   p.product_name AS product_name,
                   u.username AS ordered_by
            FROM tblpurchaseorder po
            JOIN tblsupplier s ON po.supplier_id = s.supplier_id
            JOIN tblproduct p ON po.product_id = p.product_id
            JOIN tbluser u ON po.user_id = u.user_id
            WHERE po.purchase_order_id = %s
        """, (purchase_order_id,))
        purchase_order = cursor.fetchone()
        if not purchase_order:
            raise HTTPException(status_code=404, detail="Purchase Order not found")
        return PurchaseOrderResponse(**purchase_order)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
        cursor.close()
        