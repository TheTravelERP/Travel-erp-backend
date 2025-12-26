# app/schemas/enquiry_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List


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


class EnquiryListItem(BaseModel):
    id: int

    customer_name: Optional[str]
    customer_mobile: Optional[str]
    customer_email: Optional[str]
    package_name: Optional[str]

    pax_count: int
    lead_source: str
    priority: str
    conversion_status: str

    created_at: datetime

    class Config:
        from_attributes = True 


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int

class EnquiryListResponse(BaseModel):
    data: List[EnquiryListItem]
    pagination: PaginationMeta