from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.db import Base, engine
from app.routes.auth import router as auth_router
from app.routes.estimates import router as estimates_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Vehicle Repair Estimate API", version="1.0")

# Create database tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created/verified")

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(estimates_router)

@app.get("/")
def root():
    return {"message": "Vehicle Repair Estimate API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}