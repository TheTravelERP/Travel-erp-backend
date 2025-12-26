# app/api/v1/enquiry_routes.py

from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.enquiry_schema import EnquiryCreate, EnquiryResponse, EnquiryListResponse
from app.services.enquiry_service import create_enquiry, get_enquiries
from app.utils.permission_guard import require_permission
from app.utils.request_context import get_request_context

from typing import Optional

router = APIRouter(
    prefix="/api/v1/crm/enquiries",
    tags=["CRM - Enquiries"]
)



@router.post("", response_model=EnquiryResponse)
async def create_enquiry_api(
    payload: EnquiryCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    ctx = await get_request_context(request)


    await require_permission(
        db=db,
        user_id=ctx['user_id'],
        org_id=ctx['org_id'],
        menu_key="crm_enquiries",
        action="create",
    )

    return await create_enquiry(
        db=db,
        payload=payload,
        org_id=ctx['org_id'],
        user_id=ctx['user_id'],
    )



@router.get("", response_model=EnquiryListResponse)
async def list_enquiries_api(
    request: Request,
    db: AsyncSession = Depends(get_db),

    # Pagination
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),

    # Filters
    search: Optional[str] = None,
    priority: Optional[str] = None,
    conversion_status: Optional[str] = None,
):
    # 🔐 Auth context
    ctx = await get_request_context(request)

    # 🔐 Permission check
    await require_permission(
        db=db,
        user_id=ctx["user_id"],
        org_id=ctx["org_id"],
        menu_key="crm_enquiries",
        action="view",
    )

    return await get_enquiries(
        db=db,
        org_id=ctx["org_id"],
        page=page,
        page_size=page_size,
        search=search,
        priority=priority,
        conversion_status=conversion_status,
    )