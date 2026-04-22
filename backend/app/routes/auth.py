from fastapi import APIRouter, HTTPException, status
from app.schemas import LoginRequest, TokenResponse
from app.auth import create_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):

    # For demonstration, we use hardcoded credentials
    if request.username == "admin" and request.password == "password":
        access_token = create_access_token(data={"sub": request.username})
        return TokenResponse(access_token=access_token)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )