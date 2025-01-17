from fastapi import FastAPI, HTTPException, Request
from app.routers import inventory, users
from app.database import Base, engine
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(inventory.router, prefix="/api/v1", tags=["Inventory"])

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.status_code, "hint": "Check your input or permissions"},
    )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred", "error": str(e)},
        )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management System!"}