from fastapi import APIRouter, UploadFile, File
from typing import Dict, Any
import numpy as np
import soundfile as sf
import io

from app.services.audio_analysis.audio_agent import AudioAnalysisAgent

router = APIRouter()
audio_agent = AudioAnalysisAgent()

@router.post("/analyze")
async def analyze_audio(audio_file: UploadFile = File(...)) -> Dict[str, Any]:
    """Analyze uploaded audio file"""
    # Read audio file
    audio_data, sample_rate = sf.read(io.BytesIO(await audio_file.read()))
    
    # Execute analysis
    analysis_results = await audio_agent.analyze(audio_data)
    
    return analysis_results 