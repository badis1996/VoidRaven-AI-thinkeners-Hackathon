import anthropic    
import os

# Initialize Anthropic client with API key from environment
claude_client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
    