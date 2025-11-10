import os
from dotenv import load_dotenv
from openai import OpenAI
from langsmith.wrappers import wrap_openai

load_dotenv()

# read in env variables
api_key = os.getenv("GEMINI_API_KEY")
api_base = os.getenv("GEMINI_API_BASE")
model = os.getenv("GEMINI_API_MODEL")
# Validate that required environment variables are set
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
if not api_base:
    raise ValueError("GEMINI_API_BASE environment variable is not set")
if not model:
    raise ValueError("GEMINI_API_MODEL environment variable is not set")

# Create client for Gemini API
client = wrap_openai(OpenAI(
    api_key=api_key, base_url=api_base
    ))
# Export constants
__all__ = ['client', 'api_key', 'api_base', 'model']