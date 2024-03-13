from pydantic import BaseModel, Field


class SearchForJobRequest(BaseModel):
    title: str


class SaveJobRequest(BaseModel):
    title: str
    url: str
    company: str
    source: str
    remarks: str | None = None
