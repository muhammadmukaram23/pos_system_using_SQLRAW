from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tblsales import SaleCreate, SaleResponse, SaleUpdate
from app.models.tblinvoice import InvoiceResponse
from app.models.tblproduct import ProductResponse
from typing import List
import mysql.connector

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.get("/", response_model=List[SaleResponse])
def get_sales():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.sales_id, s.invoice_id, s.product_id, 
                   s.quantity, s.unit_price,  
                   s.sub_total,
                   i.customer_id, i.payment_type, i.total_amount AS invoice_total,
                   p.product_name AS product_name
            FROM tblsales s
            JOIN tblinvoice i ON s.invoice_id = i.invoice_id
            JOIN tblproduct p ON s.product_id = p.product_id
        """)
        sales = cursor.fetchall()
        return [SaleResponse(**sale) for sale in sales]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()


@router.get("/{sales_id}", response_model=SaleResponse)
def get_sale(sales_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.sales_id, s.invoice_id, s.product_id, 
                   s.quantity, s.unit_price,  
                   s.sub_total,
                   i.customer_id, i.payment_type, i.total_amount AS invoice_total,
                   p.product_name AS product_name
            FROM tblsales s
            JOIN tblinvoice i ON s.invoice_id = i.invoice_id
            JOIN tblproduct p ON s.product_id = p.product_id
            WHERE s.sales_id = %s
        """, (sales_id,))
        sale = cursor.fetchone()
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        return SaleResponse(**sale)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(sale: SaleCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Validate invoice_id
        cursor.execute("SELECT invoice_id FROM tblinvoice WHERE invoice_id = %s", (sale.invoice_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invoice ID {sale.invoice_id} does not exist"
            )
        
        # Validate product_id
        cursor.execute("SELECT product_id FROM tblproduct WHERE product_id = %s", (sale.product_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product ID {sale.product_id} does not exist"
            )
        
        # Insert new sale
        cursor.execute("""
            INSERT INTO tblsales (invoice_id, product_id, quantity, unit_price, sub_total)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            sale.invoice_id,
            sale.product_id,
            sale.quantity,
            sale.unit_price,
            sale.sub_total
        ))
        conn.commit()
        
        # Fetch the newly created sale
        sale.sales_id = cursor.lastrowid
        return SaleResponse(**sale.dict())
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()


@router.put("/{sales_id}", response_model=SaleResponse)
def update_sale(sales_id: int, sale: SaleUpdate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if sale exists
        cursor.execute("SELECT sales_id FROM tblsales WHERE sales_id = %s", (sales_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Sale not found")
        
        # Update sale
        cursor.execute("""
            UPDATE tblsales 
            SET invoice_id = %s, product_id = %s, quantity = %s, unit_price = %s, sub_total = %s
            WHERE sales_id = %s
        """, (
            sale.invoice_id,
            sale.product_id,
            sale.quantity,
            sale.unit_price,
            sale.sub_total,
            sales_id
        ))
        conn.commit()
        
        # Fetch the updated sale
        cursor.execute("SELECT * FROM tblsales WHERE sales_id = %s", (sales_id,))
        updated_sale = cursor.fetchone()
        return SaleResponse(**updated_sale)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{sales_id}", status_code=status.HTTP_200_OK)
def delete_sale(sales_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if sale exists
        cursor.execute("SELECT sales_id FROM tblsales WHERE sales_id = %s", (sales_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Sale not found")
        
        # Delete sale
        cursor.execute("DELETE FROM tblsales WHERE sales_id = %s", (sales_id,))
        conn.commit()
        
        return {"detail": "Sale deleted successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
