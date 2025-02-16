from pydantic import BaseModel

# Pydantic models for API
class InterviewAnalysis(BaseModel):
    summary: str
    strengths: str
    weaknesses: str
    feedback: str
    topicsToDiscuss: str
