# app/api/v1/auth_routes.py
import traceback
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth_schema import OrganizationRegisterRequest, OrganizationResponse, UserResponse, LoginRequest, LoginResponse
from app.db.database import get_db
from app.services.auth_service import create_organization_with_admin, login_user
from app.utils.jwt_handler import verify_access_token;


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=OrganizationResponse)
async def register_organization(
    payload: OrganizationRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        # org, user = await create_organization_with_admin(db, payload, payload.admin)
        org, user = await create_organization_with_admin(
            db,
            payload.organization,
            payload.admin
        )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))

    return org

@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    session = await login_user(db, payload.email, payload.password)

    # set HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=session["access_token"],
        httponly=True,
        secure=False,      #  set True in production (https)
        samesite="lax",    # or "strict"
        max_age=60 * 60 * 24,  # 24 hours
    )

    # return basic info only (no token in body)
    return {
        "message": "Login successful",
        "user_id": session["user_id"],
        "org_id": session["org_id"],
        "email": payload.email,
        "org_code": session["org_code"],
    }


@router.get("/me")
async def get_me(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_access_token(token)

    return {
        "user_id": payload["user_id"],
        "org_id": payload["org_id"],
        "org_code": payload["org_code"],
        "email": payload["email"]
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}