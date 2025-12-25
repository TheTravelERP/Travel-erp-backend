from pydantic import BaseModel
from typing import Optional


class EnquiryCreate(BaseModel):
    cust_id: Optional[int]
    customer_name: Optional[str]
    customer_mobile: Optional[str]
    customer_email: Optional[str]

    pkg_id: Optional[int]
    package_name: Optional[str]

    pax_count: int
    lead_source: str
    priority: str
    conversion_status: str
    description: Optional[str]


class EnquiryResponse(EnquiryCreate):
    id: int

    class Config:
        orm_mode = True
