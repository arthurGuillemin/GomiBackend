import os
from datetime import timedelta

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    CORS_ORIGINS = [
        "http://localhost:5173",
        "https://gomiproject.netlify.app",
        "http://localhost:5174",
        "https://gomibackend.onrender.com",
    ]
    RATELIMIT_DEFAULT = "10 per minute"
    SUPABASE_KEY= os.getenv("SUPABASE_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
