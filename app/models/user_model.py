# app/models/user_model.py
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

# Python enums
class UserTypeEnum(str, Enum):
    Agent = "Agent"
    Employee = "Employee"
    Admin = "Admin"

class StatusEnum(str, Enum):
    Active = "Active"
    Inactive = "Inactive"

class PlanStatusEnum(str, Enum):
    Active = "Active"
    Inactive = "Inactive"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    reporting_to = Column(Integer, ForeignKey("user.id"), nullable=True)

    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    mobile = Column(String, nullable=True)

    # Added new
    __table_args__ = (
        UniqueConstraint("org_id", "email", name="uq_user_org_email"),
        UniqueConstraint("org_id", "mobile", name="uq_user_org_mobile"),
    )

    user_type = Column(
        SQLAEnum(UserTypeEnum, native_enum=False, length=32),
        nullable=False,
        default=UserTypeEnum.Employee,
    )
    status = Column(
        SQLAEnum(StatusEnum, native_enum=False, length=16),
        nullable=False,
        default=StatusEnum.Active,
    )
    plan_status = Column(
        SQLAEnum(PlanStatusEnum, native_enum=False, length=16),
        nullable=False,
        default=PlanStatusEnum.Active,
    )

    email_verified = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    failed_logins = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_deleted = Column(Boolean, default=False)

    # relationships
    organization = relationship("Organization", backref="users", lazy="joined")
