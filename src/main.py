from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv

from src.database import create_tables
import src.auth.router as auth_router
import src.jobs.router as job_router
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
base_router = APIRouter(prefix="/api")
create_tables()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


base_router.include_router(auth_router.router)
base_router.include_router(job_router.router)
app.include_router(base_router)
