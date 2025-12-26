# app/models/pkg_type_model.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class PackageType(Base):
    __tablename__ = "pkg_type"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)

    name = Column(String(200), nullable=False)
    description = Column(Text)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_by = Column(Integer, ForeignKey("user.id"))
    is_deleted = Column(Boolean, server_default="false")
