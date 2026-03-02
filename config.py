import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# API KEYS
# ===============================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ===============================
# MODEL SETTINGS
# ===============================

RESEARCH_MODEL = "gemini/gemini-2.5-flash"
WRITER_MODEL = "gemini/gemini-2.5-flash"
VALIDATOR_MODEL = "openrouter/deepseek/deepseek-r1"

TEMPERATURE = 0.1
MAX_TOKENS = 1200   # IMPORTANT (avoid credit errors)

# ===============================
# SYSTEM SETTINGS
# ===============================

STRICT_VERBATIM_MODE = True

ENABLE_RETRY = True
MAX_RETRY_ATTEMPTS = 1