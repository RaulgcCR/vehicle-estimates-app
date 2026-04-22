from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# --- Auth ---

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Estimate ---

class EstimateCreate(BaseModel):
    customer_name: str = Field(..., min_length=2)
    vehicle_model: str = Field(..., min_length=2)
    vehicle_year: int = Field(..., gt=1885)
    vehicle_mileage: int = Field(..., ge=0)
    repair_description: str = Field(..., min_length=5)
    estimated_cost: float = Field(..., gt=0)

class EstimateStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|approved|rejected)$")

class EstimateResponse(BaseModel):
    id: int
    customer_name: str
    vehicle_model: str
    vehicle_year: int
    vehicle_mileage: int
    repair_description: str
    estimated_cost: float
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)