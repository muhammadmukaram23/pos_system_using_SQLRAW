from fastapi import APIRouter, HTTPException, status
from app.db import get_connection
from app.models.tblreceiveproduct import ReceiveProductCreate, ReceiveProductResponse, ReceiveProductUpdate
from app.models.tblsupplier import SupplierResponse
from app.models.tblproduct import ProductResponse
from app.models.tbluser import UserResponse
from typing import List
import mysql.connector
router = APIRouter(prefix="/receive-product", tags=["Receive Product"])


