from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base

class MenuMaster(Base):
    __tablename__ = "menu_master"

    id = Column(Integer, primary_key=True)
    key = Column(String(100), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    path = Column(String(255), nullable=True)
    icon = Column(String(50), nullable=True)

    parent_id = Column(Integer, ForeignKey("menu_master.id"), nullable=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
