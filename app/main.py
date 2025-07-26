from fastapi import FastAPI
from app.routers import tblproductcategory,tblproductunit,tbluser,tblproduct,tblcustomer,tblsupplier, tblinvoice, tblsales,tblreceiveproduct,tblpurchaseorder

app = FastAPI(
    title="POS SYSTEM API",
    description="API for POS SYSTEM",
    version="1.0.0"
)

app.include_router(tblproductcategory.router)
app.include_router(tblproductunit.router)
app.include_router(tbluser.router)
app.include_router(tblproduct.router)
app.include_router(tblcustomer.router)
app.include_router(tblsupplier.router)
app.include_router(tblinvoice.router)
app.include_router(tblsales.router)
app.include_router(tblreceiveproduct.router)
app.include_router(tblpurchaseorder.router)