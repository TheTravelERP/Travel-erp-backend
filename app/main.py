# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth_routes  # ensures package init exists

app = FastAPI(title="Travel ERP API")

# allow your frontend origin (use env var in prod)
origins = [
    "http://localhost:5173",  # Vite default dev server
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] for quick dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "Travel ERP API is running!", "env": settings.ENV}
