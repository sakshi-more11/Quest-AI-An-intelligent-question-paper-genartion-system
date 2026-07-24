"""Compatibility import for legacy services; OpenRouter is the sole LLM client."""

from backend.ai_engine.question_generation.llm_client import LLMClient

__all__ = ["LLMClient"]
