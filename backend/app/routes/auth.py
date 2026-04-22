from fastapi import APIRouter, HTTPException, status
from app.schemas import LoginRequest, TokenResponse
from app.auth import create_access_token
import os

router = APIRouter(tags=["Authentication"])

# Demo credentials from environment variables
DEMO_USERNAME = os.getenv("DEMO_USERNAME", "admin")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "Admin123")

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """
    Login endpoint. For demonstration, uses credentials from environment variables.
    
    Demo credentials:
    - username: from DEMO_USERNAME env var (default: admin)
    - password: from DEMO_PASSWORD env var (default: Admin123)
    """
    # For demonstration, we use credentials from environment variables
    if request.username == DEMO_USERNAME and request.password == DEMO_PASSWORD:
        access_token = create_access_token(data={"sub": request.username})
        return TokenResponse(access_token=access_token)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )