# app/models/pkg_detail_model.py
from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class PackageDetail(Base):
    __tablename__ = "pkg_detail"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)

    description = Column(Text)
    inclusive = Column(Text)
    exclusive = Column(Text)
    brochure_path = Column(String(500))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_by = Column(Integer, ForeignKey("user.id"))
    is_deleted = Column(Boolean, server_default="false")
