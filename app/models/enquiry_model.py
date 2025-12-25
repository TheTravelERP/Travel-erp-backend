from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, DECIMAL, ForeignKey
)
from sqlalchemy.sql import func
from app.db.base import Base


class Enquiry(Base):
    __tablename__ = "enquiry"

    id = Column(Integer, primary_key=True, index=True)

    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    cust_id = Column(Integer, ForeignKey("customer.id"), nullable=True)
    pkg_id = Column(Integer, ForeignKey("pkg.id"), nullable=True)

    customer_name = Column(String(200))
    customer_mobile = Column(String(20))
    customer_email = Column(String(200))
    package_name = Column(String(200))

    pax_count = Column(Integer, nullable=False)
    lead_source = Column(String(50), nullable=False)
    priority = Column(String(20), nullable=False)
    conversion_status = Column(String(20), nullable=False)

    description = Column(Text)

    quote_amount = Column(DECIMAL(14,2))
    currency_code = Column(String(3))
    exchange_rate = Column(DECIMAL(18,8))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    created_by = Column(Integer, ForeignKey("user.id"))
    updated_by = Column(Integer, ForeignKey("user.id"))

    is_deleted = Column(Boolean, default=False)
