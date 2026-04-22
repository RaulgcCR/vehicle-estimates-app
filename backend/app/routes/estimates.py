from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.db import get_db
from app.models import Estimate
from app.schemas import (EstimateCreate, EstimateResponse, EstimateStatusUpdate)
from app.auth import verify_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/estimates", tags=["Estimates"])

@router.get("", response_model=list[EstimateResponse])
def list_estimates(status: Optional[str] = None, db: Session = Depends(get_db), user = Depends(verify_token)):
    query = db.query(Estimate).order_by(Estimate.created_at.desc())

    if status:
        query = query.filter(Estimate.status == status)

    return query.all()

@router.post("", response_model=EstimateResponse)
def create_estimate(data: EstimateCreate, db: Session = Depends(get_db), user = Depends(verify_token)):
    try:
        estimate = Estimate(
            customer_name = data.customer_name, 
            vehicle_model = data.vehicle_model, 
            vehicle_year = data.vehicle_year,
            vehicle_mileage = data.vehicle_mileage,
            repair_description = data.repair_description,
            estimated_cost = data.estimated_cost
        )
        db.add(estimate)
        db.commit()
        db.refresh(estimate)

        return estimate
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating estimate")

@router.patch("/{estimate_id}/status", response_model=EstimateResponse)
def update_estimate_status(estimate_id: int, data: EstimateStatusUpdate, db: Session = Depends(get_db), user = Depends(verify_token)):
    try:
        estimate = db.query(Estimate).filter(Estimate.id == estimate_id).first()

        if not estimate:
            raise HTTPException(status_code=404, detail=f"Estimate {estimate_id} not found")
        
        estimate.status = data.status

        db.commit()
        db.refresh(estimate)

        return estimate
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating estimate status")