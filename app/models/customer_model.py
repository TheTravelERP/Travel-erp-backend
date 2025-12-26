# app/models/customer_model.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)

    name = Column(String(200), nullable=False)
    passport_no = Column(String(50))
    email = Column(String(200))
    mobile = Column(String(20))
    gstin = Column(String(20))
    billing_address = Column(Text)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_by = Column(Integer, ForeignKey("user.id"))
    is_deleted = Column(Boolean, server_default="false")
