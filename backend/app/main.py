from fastapi import FastAPI
from app.db import Base, engine
from app.routes.auth import router as auth_router
from app.routes.estimates import router as estimates_router

app = FastAPI(title="Vehicle Repair Estimate API", version="1.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(estimates_router)

@app.get("/")
def root():
    return {"message": "API is running"}