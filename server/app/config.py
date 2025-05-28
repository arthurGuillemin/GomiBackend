import os
from datetime import timedelta

class Config:
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    CORS_ORIGINS = [
        "http://localhost:5173",
        "https://gomiproject.netlify.app"
    ]
    RATELIMIT_DEFAULT = "10 per minute"
