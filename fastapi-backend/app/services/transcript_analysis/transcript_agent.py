from typing import Dict, Any
import json
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic

from app.models.analysis import InterviewAnalysis

class TranscriptAnalysisAgent:
    def __init__(self):
        pass
    
    def analyse_transcript(self, transcript_text: str) -> Dict[str, Any]:
        model = ChatAnthropic(model='claude-3-5-sonnet-latest')
        
        prompt = """Analyze the following interview transcript and provide a structured evaluation in JSON format with the following fields:
        - summary: A brief overview of the interview
        - strengths: Key positive points observed
        - weaknesses: Areas that need improvement
        - feedback: Constructive feedback for improvement
        - topicsToDiscuss: Topics that should be discussed in follow-up

        Transcript:
        {transcript}
        
        Provide ONLY the JSON response without any additional text or explanation."""
        
        response = model.invoke(prompt.format(transcript=transcript_text))
        
        try:
            # Extract JSON from the response
            json_str = response.content
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].strip()
            
            # Parse JSON
            analysis = json.loads(json_str)
            
            # Validate against expected fields
            required_fields = ["summary", "strengths", "weaknesses", "feedback", "topicsToDiscuss"]
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = ""
                    
            return analysis
            
        except Exception as e:
            # Return a structured error response that matches expected format
            return {
                "summary": f"Error analyzing transcript: {str(e)}",
                "strengths": "",
                "weaknesses": "",
                "feedback": "",
                "topicsToDiscuss": ""
            }
