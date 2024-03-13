from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.auth.dependencies import user_dependency
from src.database import db_dependency
from src.jobs.models import Jobs
from src.jobs.schemas import SearchForJobRequest, SaveJobRequest
from src.jobs.utils import scrape_nodeflair, scrape_jobs_db
import random

router = APIRouter(
    prefix='/jobs',
    tags=['jobs']
)


@router.post("/search", )
async def search_for_jobs(request: SearchForJobRequest):
    node_flair_data = await scrape_nodeflair(request.title)
    job_db_data = await scrape_jobs_db()
    combined_list = node_flair_data + job_db_data
    random.shuffle(combined_list)
    return {
        'data': combined_list
    }

@router.get("/")
async def get_all_jobs_by_user_id(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    job_model = db.query(Jobs).filter(Jobs.user_id == user.get('id')).all()
    return job_model

@router.post("/", status_code=status.HTTP_201_CREATED)
async def save_job(user: user_dependency, db: db_dependency, request: SaveJobRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    create_job_model = Jobs(**request.dict(), user_id=user.get('id'))
    db.add(create_job_model)
    db.commit()


@router.put("/{job_id}/status")
async def update_job_status(user: user_dependency, db: db_dependency, job_id):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    job_model = db.query(Jobs).filter(Jobs.id == job_id).filter(Jobs.user_id == user.get('id')).first()
    if job_model is None:
        raise HTTPException(status_code=404, detail='Job not found')
    job_model.active = not job_model.active
    db.commit()
    return {'message': 'Item successfully Updated'}


@router.get("/{job_id}")
async def get_job_by_id(user: user_dependency, db: db_dependency, job_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    job_model = db.query(Jobs).filter(Jobs.id == job_id).filter(Jobs.user_id == user.get('id')).first()
    if job_model is None:
        raise HTTPException(status_code=404, detail='Job not found')
    return job_model
