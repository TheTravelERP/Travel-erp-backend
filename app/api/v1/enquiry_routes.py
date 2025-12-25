# app/api/v1/enquiry_routes.py

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.enquiry_schema import EnquiryCreate, EnquiryResponse
from app.services.enquiry_service import create_enquiry
from app.utils.permission_guard import require_permission
from app.utils.request_context import get_request_context

router = APIRouter(prefix="/api/v1/crm/enquiries", tags=["CRM - Enquiries"])


@router.post("", response_model=EnquiryResponse)
async def create_enquiry_api(
    payload: EnquiryCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    ctx = await get_request_context(request)

    await require_permission(
        db=db,
        user_id=user_id,
        org_id=org_id,
        menu_key="crm_enquiries",
        action="create",
    )

    return await create_enquiry(
        db=db,
        payload=payload,
        org_id=org_id,
        user_id=user_id,
    )