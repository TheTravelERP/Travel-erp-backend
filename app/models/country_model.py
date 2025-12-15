from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class CountryMaster(Base):
    __tablename__ = "country_master"

    id = Column(Integer, primary_key=True)
    iso_code = Column(String(2), unique=True, nullable=False)   # IN, SA, AE
    name = Column(String, nullable=False)
    currency_code = Column(String(3), nullable=False)          # INR, SAR, AED
