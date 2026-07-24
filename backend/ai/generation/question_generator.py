"""Legacy service adapter for OpenRouter question drafting.

The route still imports this module, so it delegates to the shared OpenRouter
client instead of constructing the removed Gemini SDK client at import time.
"""

from backend.ai_engine.question_generation.llm_client import LLMClient


def generate_questions(prompt: str):
    return LLMClient().generate(prompt)
