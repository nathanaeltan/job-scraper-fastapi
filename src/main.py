from fastapi import FastAPI
from dotenv import load_dotenv

from src.database import create_tables
import src.auth.router as auth_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
create_tables()

app.include_router(auth_router.router)
