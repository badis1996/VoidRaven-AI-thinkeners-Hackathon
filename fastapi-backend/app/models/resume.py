from typing import List, Optional
from datetime import date
from pydantic import BaseModel

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    graduation_date: Optional[date] = None

class WorkExperience(BaseModel):
    company: str
    title: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[List[str]] = []  # Changed to Optional with default empty list
    location: Optional[str] = None

class Skill(BaseModel):
    name: str

class Resume(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    education: List[Education] = []  # Changed default to empty list
    work_experience: List[WorkExperience] = []  # Changed default to empty list
    skills: List[Skill] = []  # Changed default to empty list
    certifications: List[str] = []  # Changed default to empty list
    languages: List[str] = []  # Changed default to empty list
