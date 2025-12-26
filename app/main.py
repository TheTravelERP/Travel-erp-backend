# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import router as api_v1_router  # ✅ IMPORTANT

app = FastAPI(title="Travel ERP API")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ SINGLE ENTRY POINT FOR ALL v1 APIs
app.include_router(api_v1_router)

@app.get("/")
def root():
    return {"message": "Travel ERP API is running!", "env": settings.ENV}
