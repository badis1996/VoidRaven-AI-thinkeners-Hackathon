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

@router.get("/transcript")
async def analyse_transcript():
    transcript_agent = TranscriptAnalysisAgent()
    
    transcript = """
{      "interview_date": "2025-02-16",      "interviewer": {          "name": "AI Interviewer - Paris Business School",          "role": "Admissions Assessment Agent"      },      "candidate": {          "name": "Alexandra Martin",          "email": "alex.martin@email.com",          "phone": "+33 7 56 89 34 21"      },      "transcript": [          {              "speaker": "AI Interviewer",              "text": "Good afternoon, Alexandra. Thank you for joining this interview for the Paris Business School admissions process. Can you start by telling me why you chose Paris Business School for your master's degree?"          },          {              "speaker": "Alexandra Martin",              "text": "Good afternoon! Thank you for having me. I chose Paris Business School because of its strong focus on international business and finance, areas I am deeply passionate about. The diverse student body and experienced faculty also appealed to me, as I believe they provide a dynamic learning environment."          },          {              "speaker": "AI Interviewer",              "text": "That sounds great. Can you share an experience where you demonstrated leadership during your undergraduate studies or internships?"          },          {              "speaker": "Alexandra Martin",              "text": "Certainly. During my internship at BNP Paribas, I led a project analyzing investment trends for a new client portfolio. I coordinated a team of interns, ensuring timely and accurate analysis, which contributed to a 15% increase in portfolio performance."          },          {              "speaker": "AI Interviewer",              "text": "Impressive. How do you handle challenges and pressure in a fast-paced environment?"          },          {              "speaker": "Alexandra Martin",              "text": "I prioritize tasks, stay organized, and maintain open communication with my team. At HSBC, when faced with tight deadlines, I used these strategies to ensure smooth operations and client satisfaction."          },          {              "speaker": "AI Interviewer",              "text": "Thank you, Alexandra. Lastly, how do you see yourself contributing to the Paris Business School community?"          },          {              "speaker": "Alexandra Martin",              "text": "I aim to contribute through active participation in finance and business clubs, sharing my international experience, and collaborating with peers on innovative projects."          },          {              "speaker": "AI Interviewer",              "text": "Thank you for your responses. We will be in touch with the next steps soon. Have a great day!"          },          {              "speaker": "Alexandra Martin",              "text": "Thank you! I look forward to hearing from you. Have a great day too!"          }      ]  }
    """
    text = transcript_agent.analyse_transcript(transcript)
    return text 