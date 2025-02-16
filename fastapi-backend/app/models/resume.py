from dataclasses import dataclass
from typing import List, Optional
from datetime import date

@dataclass
class Education:
    institution: str
    degree: str
    field_of_study: str
    graduation_date: Optional[date] = None
    gpa: Optional[float] = None

@dataclass
class WorkExperience:
    company: str
    title: str
    start_date: date
    end_date: Optional[date] = None
    description: List[str] = None
    location: Optional[str] = None

@dataclass
class Skill:
    name: str
    level: Optional[str] = None  # e.g., "Expert", "Intermediate", "Beginner"
    years: Optional[float] = None

@dataclass
class Resume:
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    education: List[Education] = None
    work_experience: List[WorkExperience] = None
    skills: List[Skill] = None
    certifications: List[str] = None
    languages: List[str] = None

    def __post_init__(self):
        # Initialize empty lists for None values
        if self.education is None:
            self.education = []
        if self.work_experience is None:
            self.work_experience = []
        if self.skills is None:
            self.skills = []
        if self.certifications is None:
            self.certifications = []
        if self.languages is None:
            self.languages = []
