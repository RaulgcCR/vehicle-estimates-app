from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base, engine
from app.routes.auth import router as auth_router
from app.routes.estimates import router as estimates_router

app = FastAPI(title="Vehicle Repair Estimate API", version="1.0")

Base.metadata.create_all(bind=engine)

# CORS
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(estimates_router)

@app.get("/")
def root():
    return {"message": "API is running"}