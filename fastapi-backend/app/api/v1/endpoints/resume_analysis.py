from fastapi import APIRouter, File, UploadFile
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import base64

from app.services.resume_analysis.resume_agent import ResumeAnalysisAgent
from app.services.transcript_analysis.transcript_agent import TranscriptAnalysisAgent

router = APIRouter()

@router.post("/extract")
async def read_resume(file: UploadFile = File(...)):
    pdf_data = base64.b64encode(file.file.read()).decode('utf-8')

    resume_agent = ResumeAnalysisAgent()
    
    text = resume_agent.read_resume(pdf_data)
    return text 

class TranscriptRequest(BaseModel):
    transcript: str

@router.post("/transcript")
async def analyse_transcript(request: TranscriptRequest):
    transcript_agent = TranscriptAnalysisAgent()
    text = transcript_agent.analyse_transcript(request.transcript)
    return text 