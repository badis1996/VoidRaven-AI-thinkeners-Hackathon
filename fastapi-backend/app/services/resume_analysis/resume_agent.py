from typing import Dict, Any
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic

from app.models.resume import Resume
from app.utils.llm.anthropic import claude_client

class ResumeAnalysisAgent:
    def __init__(self):
        pass

    def read_resume(self, base64_pdf: str):
        # Send to Claude
        message = claude_client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": base64_pdf
                            }
                        },
                        {
                            "type": "text",
                            "text": "Extract all text from the resume"
                        }
                    ]
                }
            ],
        )
        return self.structure_in_json(message.content)

    def structure_in_json(self, resume_text: str):

        model = ChatAnthropic(model='claude-3-5-sonnet-latest')
        parser = JsonOutputParser(pydantic_object=Resume)

        prompt = PromptTemplate(
            template="Extract all text from the resume and structure it in the following JSON format: {format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser

        return(chain.invoke({"query": resume_text}))
