import os
from .system_prompt import SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()

system_prompt = SYSTEM_PROMPT
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "cohere/north-mini-code:free"

#Backup model for necessary cases of rate limiting or model based error by the default Gemma model
FALLBACK_MODEL = "liquid/lfm-2.5-2.6b:free"
MEMORY_FILE="memory/conversations.json"

MAX_MESSAGES = 15
