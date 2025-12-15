# app/services/auth_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization_model import Organization
from app.models.user_model import User, UserTypeEnum, StatusEnum, PlanStatusEnum
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from fastapi import HTTPException, status
from app.models.country_model import CountryMaster
from sqlalchemy.orm import joinedload
from app.utils.org_utils import generate_org_code
from app.models.menu_model import MenuMaster
from app.models.user_menu_permission_model import UserMenuPermission




async def create_organization_with_admin(
    db: AsyncSession,
    org_in,
    admin_in
):
    # 1️⃣ Check org exists
    q = await db.execute(
        select(Organization).where(
            Organization.name == org_in.name,
            Organization.is_deleted == False
        )
    )
    if q.scalar_one_or_none():
        raise ValueError("Organization already exists")

    # 2️⃣ Resolve country
    res = await db.execute(
        select(CountryMaster).where(
            CountryMaster.iso_code == org_in.country_code
        )
    )
    country = res.scalar_one_or_none()
    if not country:
        raise ValueError("Invalid country selected")

    # 3️⃣ Create organization
    org = Organization(
        name=org_in.name,
        country_code=country.iso_code,
        org_code="TMP",
        base_currency=country.currency_code,
        max_users=org_in.max_users,
        max_bookings=org_in.max_bookings,
    )
    db.add(org)
    await db.flush()  # get org.id

    org.org_code = generate_org_code(org.name, org.id)

    # 4️⃣ Create admin user
    admin = User(
        org_id=org.id,
        email=admin_in.email,
        password_hash=hash_password(admin_in.password),
        mobile=admin_in.mobile,
        user_type=UserTypeEnum.Admin,
        status=StatusEnum.Active,
        plan_status=PlanStatusEnum.Active,
        email_verified=False,
    )
    db.add(admin)
    await db.flush()  # get admin.id

    # 5️⃣ FETCH ALL MENUS
    result = await db.execute(select(MenuMaster))
    menus = result.scalars().all()

    # 6️⃣ GIVE ADMIN FULL PERMISSIONS
    permissions = [
        UserMenuPermission(
            user_id=admin.id,
            menu_id=menu.id,
            can_view=True,
            can_create=True,
            can_edit=True,
            can_delete=True,
            can_export=True,
            can_import=True,
            can_print=True,
            data_scope="ORG",
        )
        for menu in menus
    ]

    db.add_all(permissions)

    # 7️⃣ COMMIT EVERYTHING
    await db.commit()
    await db.refresh(org)
    await db.refresh(admin)

    return org, admin



async def login_user(db: AsyncSession, email: str, password: str):
    query = (
        select(User,Organization)
        .join(Organization, Organization.id == User.org_id)
        .where(
            User.email == email, 
            User.is_deleted == False,
            Organization.is_deleted == False
            )
    )
    result = await db.execute(query)
    row = result.first()

    if not row:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    user, org = row

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token({
        "user_id": user.id,
        "org_id": user.org_id,
        "org_code": org.org_code,
        "email": user.email,
        "role": user.user_type.value,
    })

    return {
        "access_token": access_token,
        "user_id": user.id,
        "org_id": user.org_id,
        "org_code": org.org_code,
        "email": user.email,
    }