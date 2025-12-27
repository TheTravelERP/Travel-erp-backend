# app/api/v1/enquiry_routes.py

from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.enquiry_schema import EnquiryCreate, EnquiryResponse, EnquiryListResponse
from app.services.enquiry_service import create_enquiry, get_enquiries, get_enquiries_for_export
from app.utils.permission_guard import require_permission
from app.utils.request_context import get_request_context
from app.services.enquiry_export_service import export_csv, export_excel, export_pdf
from app.services.enquiry_import_service import import_enquiries_from_csv

from typing import Optional

# Export 
from fastapi.responses import StreamingResponse
from typing import Literal

# Import
from fastapi import UploadFile, File


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
    ctx = await get_request_context(request)

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


@router.get("/export")
async def export_enquiries_api(
    request: Request,
    format: Literal["csv", "excel", "pdf"],
    db: AsyncSession = Depends(get_db),
    search: Optional[str] = None,
    priority: Optional[str] = None,
    conversion_status: Optional[str] = None,
):
    ctx = await get_request_context(request)

    print('Hitting export api')

    await require_permission(
        db=db,
        user_id=ctx["user_id"],
        org_id=ctx["org_id"],
        menu_key="crm_enquiries",
        action="export",
    )

    rows = await get_enquiries_for_export(
        db=db,
        org_id=ctx["org_id"],
        search=search,
        priority=priority,
        conversion_status=conversion_status,
    )

    if format == "csv":
        return export_csv(rows)

    if format == "excel":
        return export_excel(rows)

    if format == "pdf":
        return export_pdf(rows)
    


@router.post("/import")
async def import_enquiries_api(
    request: Request,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    ctx = await get_request_context(request)

    await require_permission(
        db=db,
        user_id=ctx["user_id"],
        org_id=ctx["org_id"],
        menu_key="crm_enquiries",
        action="import",
    )

    result = await import_enquiries_from_csv(
        db=db,
        org_id=ctx["org_id"],
        user_id=ctx["user_id"],
        file=file,
    )

    return result
