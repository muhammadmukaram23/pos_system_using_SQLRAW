from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tblinvoice import InvoiceCreate, InvoiceResponse
from app.models.tblcustomer import CustomerResponse
from typing import List
import mysql.connector
from app.models.tbluser import UserResponse

router = APIRouter(prefix="/invoice", tags=["Invoice"])

@router.get("/", response_model=List[InvoiceResponse])
def get_invoices():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT i.invoice_id, i.customer_id, i.payment_type, 
                   i.total_amount, i.amount_tendered, 
                   i.bank_account_name, i.bank_account_number, 
                   i.date_recorded, i.user_id,
                   c.customer_name AS customer_name,
                   u.username AS created_by
            FROM tblinvoice i
            JOIN tblcustomer c ON i.customer_id = c.customer_id
            JOIN tbluser u ON i.user_id = u.user_id
        """)
        invoices = cursor.fetchall()
        return [InvoiceResponse(**invoice) for invoice in invoices]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT i.invoice_id, i.customer_id, i.payment_type, 
                   i.total_amount, i.amount_tendered, 
                   i.bank_account_name, i.bank_account_number, 
                   i.date_recorded, i.user_id,
                   c.customer_name AS customer_name,
                   u.username AS created_by
            FROM tblinvoice i
            JOIN tblcustomer c ON i.customer_id = c.customer_id
            JOIN tbluser u ON i.user_id = u.user_id
            WHERE i.invoice_id = %s
        """, (invoice_id,))
        invoice = cursor.fetchone()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return InvoiceResponse(**invoice)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(invoice: InvoiceCreate):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Validate foreign keys
        cursor.execute("SELECT customer_id FROM tblcustomer WHERE customer_id = %s", (invoice.customer_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"status": "error", "message": "Invalid customer ID"}
            )
            
        cursor.execute("SELECT user_id FROM tbluser WHERE user_id = %s", (invoice.user_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"status": "error", "message": "Invalid user ID"}
            )
        
        # Insert new invoice
        cursor.execute(
            """INSERT INTO tblinvoice (
                customer_id, payment_type, total_amount, amount_tendered,
                bank_account_name, bank_account_number, date_recorded, user_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
            (
                invoice.customer_id,
                invoice.payment_type.value,
                invoice.total_amount,
                invoice.amount_tendered,
                invoice.bank_account_name,
                invoice.bank_account_number,
                invoice.date_recorded,
                invoice.user_id
            )
        )
        conn.commit()
        invoice_id = cursor.lastrowid
        
        return InvoiceResponse(
            invoice_id=invoice_id,
            **invoice.model_dump()
        )
        
    except MySQLConnectorError as err:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": f"Database error: {err}"}
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(invoice_id: int, invoice: InvoiceCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if invoice exists
        cursor.execute("SELECT * FROM tblinvoice WHERE invoice_id = %s", (invoice_id,))
        existing_invoice = cursor.fetchone()
        if not existing_invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        # Validate foreign keys
        cursor.execute("SELECT customer_id FROM tblcustomer WHERE customer_id = %s", (invoice.customer_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"status": "error", "message": "Invalid customer ID"}
            )
            
        cursor.execute("SELECT user_id FROM tbluser WHERE user_id = %s", (invoice.user_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"status": "error", "message": "Invalid user ID"}
            )
        
        # Update invoice
        cursor.execute(
            """UPDATE tblinvoice SET 
                customer_id = %s, payment_type = %s, total_amount = %s, 
                amount_tendered = %s, bank_account_name = %s, 
                bank_account_number = %s, date_recorded = %s, user_id = %s 
            WHERE invoice_id = %s""",
            (
                invoice.customer_id,
                invoice.payment_type.value,
                invoice.total_amount,
                invoice.amount_tendered,
                invoice.bank_account_name,
                invoice.bank_account_number,
                invoice.date_recorded,
                invoice.user_id,
                invoice_id
            )
        )
        conn.commit()
        
        return InvoiceResponse(
            invoice_id=invoice_id,
            **invoice.model_dump()
        )
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
