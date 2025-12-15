# app/models/user_menu_permission_model.py
from sqlalchemy import Column, Integer, Boolean, ForeignKey, Enum, UniqueConstraint
from app.db.base import Base

class UserMenuPermission(Base):
    __tablename__ = "user_menu_permission"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menu_master.id", ondelete="CASCADE"), nullable=False)

    can_view = Column(Boolean, default=True, nullable=False)
    can_create = Column(Boolean, default=False, nullable=False)
    can_edit = Column(Boolean, default=False, nullable=False)
    can_delete = Column(Boolean, default=False, nullable=False)
    can_export = Column(Boolean, default=False, nullable=False)
    can_import = Column(Boolean, default=False, nullable=False)
    can_print = Column(Boolean, default=False, nullable=False)

    data_scope = Column(
        Enum("OWN", "TEAM", "ORG", "GLOBAL", name="data_scope_enum"),
        default="OWN",
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "menu_id", name="uq_user_menu_permission"),
    )
