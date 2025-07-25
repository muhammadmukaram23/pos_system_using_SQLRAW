from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tblcustomer import CustomerCreate, CustomerResponse
from typing import List
import mysql.connector


from app.models.tbluser import UserResponse
router = APIRouter(prefix="/customer", tags=["Customer"])

@router.get("/", response_model=List[CustomerResponse])
def get_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT customer_id, customer_code, customer_name, contact, address
            FROM tblcustomer
        """)
        customers = cursor.fetchall()
        return [CustomerResponse(**customer) for customer in customers]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT customer_id, customer_code, customer_name, contact, address FROM tblcustomer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return CustomerResponse(**customer)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if customer_code is unique
        cursor.execute("SELECT customer_id FROM tblcustomer WHERE customer_code = %s", (customer.customer_code,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with this code already exists"
            )
        
        # Insert new customer
        cursor.execute("""
            INSERT INTO tblcustomer (customer_code, customer_name, contact, address)
            VALUES (%s, %s, %s, %s)
        """, (customer.customer_code, customer.customer_name, customer.contact, customer.address))
        conn.commit()
        
        # Get the created customer ID
        customer_id = cursor.lastrowid
        
        # Fetch the created customer details
        cursor.execute("SELECT * FROM tblcustomer WHERE customer_id = %s", (customer_id,))
        new_customer = cursor.fetchone()
        
        return CustomerResponse(**new_customer)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if customer exists
        cursor.execute("SELECT customer_id FROM tblcustomer WHERE customer_id = %s", (customer_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Update customer details
        cursor.execute("""
            UPDATE tblcustomer 
            SET customer_code = %s, customer_name = %s, contact = %s, address = %s 
            WHERE customer_id = %s
        """, (customer.customer_code, customer.customer_name, customer.contact, customer.address, customer_id))
        conn.commit()
        
        # Fetch the updated customer details
        cursor.execute("SELECT * FROM tblcustomer WHERE customer_id = %s", (customer_id,))
        updated_customer = cursor.fetchone()
        
        return CustomerResponse(**updated_customer)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{customer_id}", status_code=status.HTTP_200_OK)
def delete_customer(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if customer exists
        cursor.execute("SELECT customer_id FROM tblcustomer WHERE customer_id = %s", (customer_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Delete customer
        cursor.execute("DELETE FROM tblcustomer WHERE customer_id = %s", (customer_id,))
        conn.commit()
        
        return {"detail": "Customer deleted successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
