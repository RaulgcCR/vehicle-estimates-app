from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .db import Base

class Estimate(Base):
    __tablename__ = "estimates"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    vehicle_model = Column(String, nullable=False)
    vehicle_year = Column(Integer, index=True)
    vehicle_mileage = Column(Integer, index=True)
    repair_description = Column(String, nullable=False)
    estimated_cost = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)