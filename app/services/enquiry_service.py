# app/services/enquiry_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.enquiry_model import Enquiry
from app.schemas.enquiry_schema import EnquiryCreate, EnquiryListResponse, PaginationMeta

from sqlalchemy import select, func, or_
from typing import Optional


async def create_enquiry(
    db: AsyncSession,
    payload: EnquiryCreate,
    org_id: int,
    user_id: int,
):
    enquiry = Enquiry(
        org_id=org_id,          
        agent_id=user_id, 

        cust_id=payload.cust_id,
        pkg_id=payload.pkg_id,

        customer_name=payload.customer_name,
        customer_mobile=payload.customer_mobile,
        customer_email=payload.customer_email,
        package_name=payload.package_name,

        pax_count=payload.pax_count,
        lead_source=payload.lead_source,
        priority=payload.priority,
        conversion_status=payload.conversion_status,
        description=payload.description,

        created_by=user_id,
    )

    db.add(enquiry)
    await db.commit()
    await db.refresh(enquiry)

    return enquiry


async def get_enquiries(
    db: AsyncSession,
    org_id: int,
    page: int,
    page_size: int,
    search: Optional[str],
    priority: Optional[str],
    conversion_status: Optional[str],
):
    # Base query (ORG ISOLATION)
    base_query = select(Enquiry).where(
        Enquiry.org_id == org_id,
        Enquiry.is_deleted == False
    )

    if search:
        base_query = base_query.where(
            or_(
                Enquiry.customer_name.ilike(f"%{search}%"),
                Enquiry.customer_mobile.ilike(f"%{search}%"),
                Enquiry.customer_email.ilike(f"%{search}%"),
                Enquiry.package_name.ilike(f"%{search}%"),
            )
        )

    if priority:
        base_query = base_query.where(Enquiry.priority == priority)

    if conversion_status:
        base_query = base_query.where(Enquiry.conversion_status == conversion_status)


    count_stmt = select(func.count()).select_from(base_query.subquery())
    total = await db.scalar(count_stmt)


    offset = (page - 1) * page_size
    paged_query = (
        base_query
        .order_by(Enquiry.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )

    result = await db.execute(paged_query)
    enquiries = result.scalars().all()

    return EnquiryListResponse(
        data=enquiries,
        pagination=PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
        )
    )



async def get_enquiries_for_export(
    db: AsyncSession,
    org_id: int,
    search: Optional[str],
    priority: Optional[str],
    conversion_status: Optional[str],
):
    query = select(Enquiry).where(
        Enquiry.org_id == org_id,
        Enquiry.is_deleted == False
    )

    if search:
        query = query.where(
            or_(
                Enquiry.customer_name.ilike(f"%{search}%"),
                Enquiry.customer_mobile.ilike(f"%{search}%"),
                Enquiry.customer_email.ilike(f"%{search}%"),
                Enquiry.package_name.ilike(f"%{search}%"),
            )
        )

    if priority:
        query = query.where(Enquiry.priority == priority)

    if conversion_status:
        query = query.where(Enquiry.conversion_status == conversion_status)

    query = query.order_by(Enquiry.created_at.desc())

    result = await db.execute(query)
    return result.scalars().all()
