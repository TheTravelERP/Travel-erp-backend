# app/api/v1/navigation_routes.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.navigation_service import get_user_navigation
from app.utils.jwt_handler import verify_access_token

router = APIRouter(
    prefix="/api/v1/me",
    tags=["navigation"]
)



@router.get("/navigation")
async def my_navigation(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_access_token(token)

    # ✅ org_id & user_id come from JWT
    user_id = payload["user_id"]
    org_id = payload["org_id"]

    return await get_user_navigation(db, user_id, org_id)
