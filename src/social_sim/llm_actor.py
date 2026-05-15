from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


ROOT = Path(__file__).resolve().parents[2]


class LLMProviderError(RuntimeError):
    pass


@dataclass(frozen=True)
class LLMRequest:
    system_prompt: str
    user_prompt: str
    schema_name: str
    schema: dict[str, Any]


@dataclass(frozen=True)
class LLMResponse:
    text: str
    raw_response: dict[str, Any]
    provider: str
    model: str


class LLMProvider(Protocol):
    provider: str
    model: str

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


class OpenAIResponsesProvider:
    provider = "openai"

    def __init__(self, api_key: str, model: str = "gpt-4.1-mini") -> None:
        if not api_key:
            raise LLMProviderError("OPENAI_API_KEY is required")
        self.api_key = api_key
        self.model = model

    @classmethod
    def from_env(cls, dotenv_path: Path | None = None, model: str | None = None) -> "OpenAIResponsesProvider":
        if dotenv_path is not None:
            load_dotenv(dotenv_path)
        api_key = os.environ.get("OPENAI_API_KEY", "")
        selected_model = model or os.environ.get("OPENAI_MODEL") or "gpt-4.1-mini"
        return cls(api_key=api_key, model=selected_model)

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        payload = {
            "model": self.model,
            "input": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": request.schema_name,
                    "schema": request.schema,
                    "strict": False,
                }
            },
        }
        raw = self._post_json("https://api.openai.com/v1/responses", payload)
        text = extract_response_text(raw)
        return LLMResponse(text=text, raw_response=raw, provider=self.provider, model=self.model)

    def _post_json(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise LLMProviderError(
                f"OpenAI Responses API returned HTTP {exc.code}: {redact_api_keys(error_body)}"
            ) from exc
        except urllib.error.URLError as exc:
            raise LLMProviderError(f"OpenAI Responses API request failed: {exc}") from exc


def extract_response_text(response: dict[str, Any]) -> str:
    if isinstance(response.get("output_text"), str):
        return response["output_text"]

    texts: list[str] = []
    for item in response.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and isinstance(content.get("text"), str):
                texts.append(content["text"])
    if texts:
        return "\n".join(texts)
    raise LLMProviderError("OpenAI response did not contain output text")


def redact_api_keys(text: str) -> str:
    return re.sub(r"sk-[A-Za-z0-9_*.-]+", "sk-...redacted", text)
