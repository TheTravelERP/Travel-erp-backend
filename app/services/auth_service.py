# app/services/auth_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization_model import Organization
from app.models.user_model import User, UserTypeEnum, StatusEnum, PlanStatusEnum
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from fastapi import HTTPException, status


async def create_organization_with_admin(db: AsyncSession, org_in, admin_in):
    """
    org_in: pydantic OrganizationCreate
    admin_in: pydantic AdminCreate
    """
    # check existing name
    q = await db.execute(
        select(Organization).where(Organization.name == org_in.name, Organization.is_deleted == False)
    )
    existing = q.scalar_one_or_none()
    if existing:
        raise ValueError("Organization already exists")

    # create organization
    org = Organization(
        name=org_in.name,
        base_currency=org_in.base_currency,
        max_users=org_in.max_users,
        max_bookings=org_in.max_bookings,
    )
    db.add(org)
    await db.flush()  # ensure org.id is available

    # create admin user
    user = User(
        org_id=org.id,
        reporting_to=None,
        email=admin_in.email,
        password_hash=hash_password(admin_in.password),
        mobile=admin_in.mobile,
        user_type=UserTypeEnum.Admin,
        status=StatusEnum.Active,
        plan_status=PlanStatusEnum.Active,
        email_verified=False,
    )
    db.add(user)

    await db.commit()
    # refresh to get DB-generated fields
    await db.refresh(org)
    await db.refresh(user)
    return org, user


async def login_user(db: AsyncSession, email: str, password: str):
    query = select(User).where(User.email == email, User.is_deleted == False)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token({
        "user_id": user.id,
        "org_id": user.org_id,
        "email": user.email
    })

    return {
        "access_token": access_token,
        "user_id": user.id,
        "org_id": user.org_id,
        "email": user.email
    }