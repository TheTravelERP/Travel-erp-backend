# app/models/pkg_model.py
from sqlalchemy import (
    Column, Integer, String, Date, Boolean,
    ForeignKey, DateTime, Numeric
)
from sqlalchemy.sql import func
from app.db.base import Base

class Package(Base):
    __tablename__ = "pkg"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)

    pkg_type_id = Column(Integer, ForeignKey("pkg_type.id"))
    pkg_detail_id = Column(Integer, ForeignKey("pkg_detail.id"))

    code = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)

    total_seats = Column(Integer)
    booked_seats = Column(Integer, server_default="0")

    depart_date = Column(Date)
    arrive_date = Column(Date)
    depart_city = Column(String(100))
    no_of_days = Column(Integer)

    single_amt = Column(Numeric(14, 2))
    currency_code = Column(String(3))
    exchange_rate = Column(Numeric(18, 8))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_by = Column(Integer, ForeignKey("user.id"))
    is_deleted = Column(Boolean, server_default="false")
