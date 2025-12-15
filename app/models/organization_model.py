# app/models/organization_model.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    # Added new
    org_code = Column(String(10), nullable=True, unique=True, index=True)

    country_code = Column(String(2), nullable=False)
    base_currency = Column(String(3), nullable=False)

    max_users = Column(Integer, default=50)
    max_bookings = Column(Integer, default=1000)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_deleted = Column(Boolean, default=False)
