# app/api/v1/__init__.py
from fastapi import APIRouter

from .auth_routes import router as auth_router
from .navigation_routes import router as navigation_router
from .enquiry_routes import router as enquiry_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(navigation_router)
router.include_router(enquiry_router)
