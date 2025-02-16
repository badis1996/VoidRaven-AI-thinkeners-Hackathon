from typing import Dict, Any
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic

from app.models.analysis import InterviewAnalysis

class TranscriptAnalysisAgent:
    def __init__(self):
        pass
    
    def analyse_transcript(self, transcript_text: str):

        model = ChatAnthropic(model='claude-3-5-sonnet-latest')
        parser = JsonOutputParser(pydantic_object=InterviewAnalysis)

        prompt = PromptTemplate(
            template="analyse the transcript and extract the following information: {format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser

        return(chain.invoke({"query": transcript_text}))
