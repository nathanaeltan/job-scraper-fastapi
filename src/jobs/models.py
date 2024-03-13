from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from src.database import Base


class Jobs(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    url = Column(String)
    company = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    active = Column(Boolean, default=True)
    remarks = Column(String, nullable=True)
    source = Column(String)
