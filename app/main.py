# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth_routes, navigation_routes  # 👈 ADD THIS

app = FastAPI(title="Travel ERP API")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 REGISTER ROUTERS
app.include_router(auth_routes.router)
app.include_router(navigation_routes.router)   # 👈 ADD THIS

@app.get("/")
def root():
    return {"message": "Travel ERP API is running!", "env": settings.ENV}
