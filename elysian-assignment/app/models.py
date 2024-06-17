import uuid
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, UUID4
from typing import Optional, Dict
from datetime import datetime

Base = declarative_base()

# SQLAlchemy Model
class Person(Base):
    __tablename__ = "people"

    id = Column(VARCHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=text("UUID()"))
    name = Column(String(255), index=True)

# Pydantic Models
class PersonBase(BaseModel):
    id: UUID4
    name: str

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLAlchemy models

class PersonAdded(BaseModel):
    person_id: UUID4
    name: str
    timestamp: datetime

class PersonRenamed(BaseModel):
    person_id: UUID4
    name: str
    timestamp: datetime

class PersonRemoved(BaseModel):
    person_id: UUID4
    timestamp: datetime

class WebhookPayload(BaseModel):
    payload_type: str
    payload_content: Dict
    
class GetNameResponse(BaseModel):
    name: Optional[str]

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLAlchemy models