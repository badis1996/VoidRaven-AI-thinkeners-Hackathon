from typing import Dict, Any
import anthropic
import base64
import httpx

class ResumeAnalysisAgent:
    def __init__(self):
        pass

    def read_resume(self, base64_pdf: str):
        # Send to Claude
        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
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
        return(message.content)

