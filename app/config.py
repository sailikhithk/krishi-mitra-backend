import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/krishimitra")
SECRET_KEY = os.getenv("SECRET_KEY", "postgres")
