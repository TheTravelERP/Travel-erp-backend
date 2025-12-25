from sqlalchemy.ext.asyncio import AsyncSession
from app.models.enquiry_model import Enquiry
from app.schemas.enquiry_schema import EnquiryCreate


async def create_enquiry(
    db: AsyncSession,
    payload: EnquiryCreate,
    org_id: int,
    user_id: int
):
    enquiry = Enquiry(
        org_id=org_id,
        agent_id=user_id,
        created_by=user_id,
        **payload.dict()
    )

    db.add(enquiry)
    await db.commit()
    await db.refresh(enquiry)
    return enquiry
