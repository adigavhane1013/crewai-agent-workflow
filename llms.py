import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

def get_gemini_llm():
    return LLM(
        model="ollama/phi3",
        base_url="http://localhost:11434",
        temperature=0.1,
        max_tokens=1200
    )

def get_validator_llm():
    return LLM(
        model="ollama/phi3",
        base_url="http://localhost:11434",
        temperature=0.0,
        max_tokens=300
    )