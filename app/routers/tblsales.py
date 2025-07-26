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
            SELECT s.sales_id, s.invoice_id, s.product_id, s.quantity, 
                   s.unit_price, s.sub_total, i.date_recorded,
                   i.invoice_id AS invoice_number,
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
            SELECT s.sales_id, s.invoice_id, s.product_id, s.quantity, 
                   s.unit_price, s.sub_total, i.date_recorded,
                   i.invoice_id AS invoice_number,
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
        cursor.execute("""
            INSERT INTO tblsales (invoice_id, product_id, quantity, 
                                  unit_price, sub_total)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            sale.invoice_id,
            sale.product_id,
            sale.quantity,
            sale.unit_price,
            sale.sub_total
        ))
        conn.commit()
        sales_id = cursor.lastrowid
        
        # Fetch the newly created sale
        cursor.execute("SELECT * FROM tblsales WHERE sales_id = %s", (sales_id,))
        new_sale = cursor.fetchone()
        return SaleResponse(**new_sale)
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

        update_fields = []
        update_values = []

        if sale.invoice_id is not None:
            update_fields.append("invoice_id = %s")
            update_values.append(sale.invoice_id)
        if sale.product_id is not None:
            update_fields.append("product_id = %s")
            update_values.append(sale.product_id)
        if sale.quantity is not None:
            update_fields.append("quantity = %s")
            update_values.append(sale.quantity)
        if sale.unit_price is not None:
            update_fields.append("unit_price = %s")
            update_values.append(sale.unit_price)
        if sale.sub_total is not None:
            update_fields.append("sub_total = %s")
            update_values.append(sale.sub_total)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_query = f"UPDATE tblsales SET {', '.join(update_fields)} WHERE sales_id = %s"
        update_values.append(sales_id)

        cursor.execute(update_query, tuple(update_values))
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

        cursor.execute("DELETE FROM tblsales WHERE sales_id = %s", (sales_id,))
        conn.commit()
        return {"status": "success", "message": "Sale deleted successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()