from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tblproduct import ProductCreate, ProductResponse
from app.models.tblproductcategory import ProductCategoryResponse
from app.models.tblproductunit import ProductUnitResponse
from typing import List
import mysql.connector

router = APIRouter(prefix="/product", tags=["Product"])

@router.get("/", response_model=List[ProductResponse])
def get_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.product_id, p.produce_code, p.product_name, 
                   p.unit_id, p.category_id, p.user_id, 
                   pu.unit_name AS unit, pc.category_name AS category, 
                   p.unit_in_stock, p.unit_price, 
                   p.discount_percentage, p.reorder_level, 
                   u.username AS created_by
            FROM tblproduct p
            JOIN tblproductunit pu ON p.unit_id = pu.unit_id
            JOIN tblproductcategory pc ON p.category_id = pc.category_id
            JOIN tbluser u ON p.user_id = u.user_id
        """)
        products = cursor.fetchall()
        return [ProductResponse(**product) for product in products]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 1. Check if produce_code is unique
        cursor.execute(
            "SELECT product_id FROM tblproduct WHERE produce_code = %s", 
            (product.produce_code,)
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this produce code already exists"
            )
        
        # 2. Validate unit_id
        cursor.execute("SELECT unit_id FROM tblproductunit WHERE unit_id = %s", (product.unit_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unit ID {product.unit_id} does not exist"
            )
        
        # 3. Validate category_id
        cursor.execute("SELECT category_id FROM tblproductcategory WHERE category_id = %s", (product.category_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category ID {product.category_id} does not exist"
            )
        
        # 4. Validate user_id
        cursor.execute("SELECT user_id FROM tbluser WHERE user_id = %s", (product.user_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User ID {product.user_id} does not exist"
            )

        # 5. Insert new product
        cursor.execute(
            """
            INSERT INTO tblproduct (produce_code, product_name, unit_id, 
                                    category_id, unit_in_stock, unit_price, 
                                    discount_percentage, reorder_level, user_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, 
            (product.produce_code, product.product_name, product.unit_id,
             product.category_id, product.unit_in_stock, product.unit_price,
             product.discount_percentage, product.reorder_level, product.user_id)
        )
        conn.commit()
        
        # 6. Fetch and return the newly created product
        new_product_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tblproduct WHERE product_id = %s", (new_product_id,))
        new_product = cursor.fetchone()
        
        return ProductResponse(**new_product)

    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {err}"
        )
    finally:
        cursor.close()
        conn.close()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM tblproduct WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductResponse(**product)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if product exists
        cursor.execute("SELECT product_id FROM tblproduct WHERE product_id = %s", (product_id,))
        existing_product = cursor.fetchone()
        
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Validate unit_id
        cursor.execute("SELECT unit_id FROM tblproductunit WHERE unit_id = %s", (product.unit_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unit ID {product.unit_id} does not exist"
            )
        
        # Validate category_id
        cursor.execute("SELECT category_id FROM tblproductcategory WHERE category_id = %s", (product.category_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category ID {product.category_id} does not exist"
            )
        
        # Validate user_id
        cursor.execute("SELECT user_id FROM tbluser WHERE user_id = %s", (product.user_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User ID {product.user_id} does not exist"
            )

        # Update product details
        cursor.execute(
            """
            UPDATE tblproduct 
            SET produce_code = %s, product_name = %s, unit_id = %s, 
                category_id = %s, unit_in_stock = %s, unit_price = %s, 
                discount_percentage = %s, reorder_level = %s, user_id = %s 
            WHERE product_id = %s
            """, 
            (product.produce_code, product.product_name, product.unit_id,
             product.category_id, product.unit_in_stock, product.unit_price,
             product.discount_percentage, product.reorder_level, product.user_id, product_id)
        )
        conn.commit()
        
        # Fetch and return the updated product
        cursor.execute("SELECT * FROM tblproduct WHERE product_id = %s", (product_id,))
        updated_product = cursor.fetchone()
        
        return ProductResponse(**updated_product)

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if product exists
        cursor.execute("SELECT product_id FROM tblproduct WHERE product_id = %s", (product_id,))
        existing_product = cursor.fetchone()
        
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Delete product
        cursor.execute("DELETE FROM tblproduct WHERE product_id = %s", (product_id,))
        conn.commit()
        
        return {"detail": "Product deleted successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

