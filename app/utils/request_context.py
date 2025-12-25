# app/utils/request_context.py
from fastapi import Request, HTTPException, status
from app.utils.jwt_handler import verify_access_token

async def get_request_context(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_access_token(token)

    return {
        "user_id": payload["user_id"],
        "org_id": payload["org_id"],
        "org_code": payload.get("org_code"),
    }
