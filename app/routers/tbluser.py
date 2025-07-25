from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tbluser import UserCreate, UserResponse
from typing import List
import mysql.connector

router=APIRouter(prefix="/user", tags=["User"])
@router.get("/", response_model=List[UserResponse])
def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, username, fullname, designation, contact, account_type FROM tbluser")
        users = cursor.fetchall()
        return [UserResponse(**user) for user in users]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, username, fullname, designation, contact, account_type FROM tbluser WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(**user)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # First check if username already exists
        cursor.execute(
            "SELECT user_id FROM tbluser WHERE username = %s", 
            (user.username,)
        )
        existing_user = cursor.fetchone()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Insert new user if username is unique
        cursor.execute(
            "INSERT INTO tbluser (username, password, fullname, designation, contact, account_type) VALUES (%s, %s, %s, %s, %s, %s)", 
            (user.username, user.password, user.fullname, user.designation.value, user.contact, user.account_type.value)
        )
        conn.commit()
        
        # Get the ID of the newly created user
        user_id = cursor.lastrowid
        
        # Fetch the newly created user details
        cursor.execute("SELECT user_id, username, fullname, designation, contact, account_type FROM tbluser WHERE user_id = %s", (user_id,))
        new_user = cursor.fetchone()
        
        return UserResponse(**new_user)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if user exists
        cursor.execute("SELECT user_id FROM tbluser WHERE user_id = %s", (user_id,))
        existing_user = cursor.fetchone()
        
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update user details
        cursor.execute(
            "UPDATE tbluser SET username = %s, fullname = %s, designation = %s, contact = %s, account_type = %s WHERE user_id = %s",
            (user.username, user.fullname, user.designation.value, user.contact, user.account_type.value, user_id)
        )
        conn.commit()
        
        # Fetch the updated user details
        cursor.execute("SELECT user_id, username, fullname, designation, contact, account_type FROM tbluser WHERE user_id = %s", (user_id,))
        updated_user = cursor.fetchone()
        
        return UserResponse(**updated_user)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if user exists
        cursor.execute("SELECT user_id FROM tbluser WHERE user_id = %s", (user_id,))
        existing_user = cursor.fetchone()
        
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Delete the user
        cursor.execute("DELETE FROM tbluser WHERE user_id = %s", (user_id,))
        conn.commit()
        
        return {"detail": "User deleted successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()