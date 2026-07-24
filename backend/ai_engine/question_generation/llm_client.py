"""Small OpenRouter client used exclusively for question drafting.

OpenRouter implements the OpenAI chat-completions wire format.  Keeping this
adapter dependency-free makes it usable in the current deployment image and
easy to replace in tests.
"""

import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class LLMClient:
    endpoint = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key=None, model=None, timeout=60):
        self.api_key = api_key if api_key is not None else os.getenv("OPENROUTER_API_KEY")
        # Do not silently route a configured institution model to another
        # provider/model.  Question generation must be reproducible.
        # Free router selects an available free model that supports the
        # requested JSON response format.  Unlike a fixed free-model slug it
        # does not break whenever a provider retires a model.
        self.model = model or os.getenv("OPENROUTER_MODEL", "openrouter/free")
        self.timeout = timeout

    def generate(self, prompt, *, retry=False):
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not configured")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Return only the requested valid JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.35,
            # A 40-item bank is commonly cut off by provider defaults.  A
            # cut-off JSON string is not recoverable, so reserve enough room
            # for the requested response rather than relying on a default.
            "max_tokens": 8000,
            "response_format": {"type": "json_object"},
        }
        request = Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenRouter request failed ({exc.code}): {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"OpenRouter is unavailable: {exc.reason}") from exc
        try:
            content = body["choices"][0]["message"].get("content")
            if not isinstance(content, str) or not content.strip():
                raise ValueError("completion content was empty")
            return content
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("OpenRouter returned an invalid completion payload") from exc

    def generate_json(self, prompt, required_key=None, minimum_items=None):
        """Return a JSON completion, retrying once when a provider truncates it.

        JSON mode is advisory across OpenRouter providers.  This boundary is
        deliberately the single place that normalises harmless wrappers and
        turns malformed output into a retry instead of a 500 from ``json``.
        """
        errors = []
        original_prompt = prompt
        for attempt in range(2):
            content = self.generate(prompt, retry=bool(attempt))
            try:
                payload = self._parse_json(content)
                if required_key and (not isinstance(payload, dict) or required_key not in payload):
                    raise ValueError("JSON response did not contain '%s'" % required_key)
                if minimum_items is not None and not isinstance(payload[required_key], list):
                    raise ValueError("JSON response field '%s' was not an array" % required_key)
                if minimum_items is not None and len(payload[required_key]) < minimum_items:
                    raise ValueError("JSON response contained fewer than %d '%s' items" %
                                     (minimum_items, required_key))
                return payload
            except (ValueError, json.JSONDecodeError) as exc:
                errors.append(str(exc))
                # Retain the original material because a repair instruction
                # without it cannot reproduce the requested questions.
                prompt = original_prompt + (
                    "\n\nRETRY REQUIREMENT: The previous response failed validation "
                    "(%s). Return a compact complete JSON object only; no Markdown, "
                    "comments, or text outside JSON." % exc
                )
        raise ValueError("OpenRouter returned malformed JSON after retry: " + errors[-1])

    @staticmethod
    def _parse_json(content):
        text = str(content or "").strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        # Some providers prepend a sentence despite JSON mode. Extract the
        # first complete object/array without trying to guess a truncated one.
        start = next((i for i, char in enumerate(text) if char in "[{"), -1)
        if start < 0:
            raise ValueError("completion did not contain JSON")
        decoder = json.JSONDecoder()
        try:
            value, _ = decoder.raw_decode(text[start:])
            return value
        except json.JSONDecodeError:
            # Accept a common, non-semantic defect while refusing unsafe
            # repairs such as inventing a closing quote for a truncated item.
            repaired = re.sub(r",\s*([}\]])", r"\1", text[start:])
            return json.loads(repaired)
