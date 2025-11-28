from fastapi import APIRouter
from app.db.database import AsyncSessionLocal
from sqlalchemy import text

router = APIRouter()

@router.get("/test-db")
async def test_db():
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            return {"status": "ok", "value": value}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
