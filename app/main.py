from fastapi import FastAPI, HTTPException, Request
from app.routers import inventory, users
from app.database import Base, engine
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

# Initialize logging
logger = logging.getLogger("uvicorn.error")

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(inventory.router)

# Custom exception handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.status_code, "hint": "Check your input or permissions"},
    )

# Middleware for processing time and error handling
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred", "error": str(e)},
        )

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

# Welcome route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management System!"}
