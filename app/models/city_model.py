from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class CityMaster(Base):
    __tablename__ = "city_master"

    id = Column(Integer, primary_key=True)
    country_code = Column(String(2), nullable=False, index=True)
    city_code = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        # Prevent duplicate cities in same country
        {"sqlite_autoincrement": True},
    )
