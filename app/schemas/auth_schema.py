# app/schemas/auth_schema.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import traceback

class OrganizationCreate(BaseModel):
    name: str = Field(..., example="Acme Travels")
    country_code: str
    # base_currency: Optional[str] = Field("INR", max_length=3)
    max_users: Optional[int] = 50
    max_bookings: Optional[int] = 1000


class AdminCreate(BaseModel):
    admin_name: str
    email: EmailStr
    mobile: Optional[str]
    password: str = Field(..., min_length=8)

class OrganizationRegisterRequest(BaseModel):
    organization: OrganizationCreate
    admin: AdminCreate

class OrganizationResponse(BaseModel):
    id: int
    name: str
    country_code: str
    base_currency: Optional[str]
    max_users: int
    max_bookings: int

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    user_type: str

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int
    org_id: int
    org_code: str
