from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tblproductcategory import ProductCategoryCreate, ProductCategoryResponse
from typing import List
import mysql.connector

router = APIRouter(prefix="/product-category", tags=["Product Category"])

@router.get("/", response_model=List[ProductCategoryResponse])
def get_product_categories():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT category_id, category_name FROM tblproductcategory")
        categories = cursor.fetchall()
        return [ProductCategoryResponse(**category) for category in categories]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{category_id}", response_model=ProductCategoryResponse)
def get_product_category(category_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT category_id, category_name FROM tblproductcategory WHERE category_id = %s", (category_id,))
        category = cursor.fetchone()
        if not category:
            raise HTTPException(status_code=404, detail="Product category not found")
        return ProductCategoryResponse(**category)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=ProductCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_product_category(category: ProductCategoryCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # First check if category with same name already exists
        cursor.execute(
            "SELECT category_id FROM tblproductcategory WHERE category_name = %s", 
            (category.category_name,)
        )
        existing_category = cursor.fetchone()
        
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
        
        # Insert new category if name is unique
        cursor.execute(
            "INSERT INTO tblproductcategory (category_name) VALUES (%s)", 
            (category.category_name,)
        )
        conn.commit()
        category_id = cursor.lastrowid
        
        return ProductCategoryResponse(
            category_id=category_id, 
            category_name=category.category_name
        )
        
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {err}"
        )
    finally:
        cursor.close()
        conn.close()


@router.put("/{category_id}", response_model=ProductCategoryResponse)
def update_product_category(category_id: int, category: ProductCategoryCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if category exists
        cursor.execute(
            "SELECT category_id FROM tblproductcategory WHERE category_id = %s", 
            (category_id,)
        )
        existing_category = cursor.fetchone()
        
        if not existing_category:
            raise HTTPException(status_code=404, detail="Product category not found")
        
        # Update category name
        cursor.execute(
            "UPDATE tblproductcategory SET category_name = %s WHERE category_id = %s", 
            (category.category_name, category_id)
        )
        conn.commit()
        
        return ProductCategoryResponse(
            category_id=category_id, 
            category_name=category.category_name
        )
        
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {err}"
        )
    finally:
        cursor.close()
        conn.close()

@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_product_category(category_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if category exists
        cursor.execute(
            "SELECT category_id FROM tblproductcategory WHERE category_id = %s", 
            (category_id,)
        )
        existing_category = cursor.fetchone()
        
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Product category not found"
            )
        
        # Delete category
        cursor.execute(
            "DELETE FROM tblproductcategory WHERE category_id = %s", 
            (category_id,)
        )
        conn.commit()
        
        return {"message": "Product category deleted successfully"}
    
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {err}"
        )
    
    finally:
        cursor.close()
        conn.close()
