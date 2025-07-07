from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
import os

app = FastAPI(title="Jewelry Products API", version="1.0.0")

# CORS middleware for production
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:8080", 
    "https://*.onrender.com",
    "https://*.netlify.app",
    "https://*.vercel.app"
]

# If in production, allow all origins for simplicity
if os.getenv("RENDER"):
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)