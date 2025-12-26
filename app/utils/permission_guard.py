# app/utils/permission_guard.py
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_menu_permission_model import UserMenuPermission
from app.models.menu_model import MenuMaster

async def require_permission(
    db: AsyncSession,
    user_id: int,
    org_id: int,
    menu_key: str,
    action: str,
):
    
    print('user_id', user_id, 'org_id', org_id, 'menu_key', menu_key, 'action', action)
    stmt = (
        select(UserMenuPermission)
        .join(MenuMaster, MenuMaster.id == UserMenuPermission.menu_id)
        .where(
            UserMenuPermission.user_id == user_id,
            MenuMaster.key == menu_key,
            getattr(UserMenuPermission, f"can_{action}") == True,
        )
    )

    res = await db.execute(stmt)
    perm = res.scalar_one_or_none()

    if not perm:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
