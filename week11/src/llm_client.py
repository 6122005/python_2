"""Unified, retry-safe LLM client supporting Groq and Anthropic.

Defaults to Groq if GROQ_API_KEY is available (model: openai/gpt-oss-20b),
or Anthropic if ANTHROPIC_API_KEY is present.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class TextBlock:
    text: str
    type: str = "text"


@dataclass
class ToolUseBlock:
    id: str
    name: str
    input: Dict[str, Any]
    type: str = "tool_use"


@dataclass
class LLMResponse:
    content: List[Any] = field(default_factory=list)


class LLMClient:
    """Wraps Groq or Anthropic with retries and a uniform block-based interface."""

    def __init__(
        self,
        model: str | None = None,
        max_tokens: int = 1024,
        max_retries: int = 3,
        api_key: Optional[str] = None,
    ) -> None:
        groq_key = api_key or os.environ.get("GROQ_API_KEY")
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

        if groq_key:
            from groq import Groq
            self.provider = "groq"
            self._client = Groq(api_key=groq_key)
            self.model = model or "openai/gpt-oss-20b"
        elif anthropic_key:
            import anthropic
            self.provider = "anthropic"
            self._client = anthropic.Anthropic(api_key=anthropic_key)
            self.model = model or "claude-sonnet-4-5"
        else:
            raise RuntimeError(
                "Neither GROQ_API_KEY nor ANTHROPIC_API_KEY is set in .env. "
                "Please set GROQ_API_KEY."
            )

        self.max_tokens = max_tokens
        self.max_retries = max_retries

    def send(
        self,
        messages: List[Dict[str, Any]],
        system: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        """Call the API with exponential backoff on transient errors."""
        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                if self.provider == "groq":
                    return self._send_groq(messages, system, tools)
                else:
                    return self._send_anthropic(messages, system, tools)
            except Exception as exc:
                last_error = exc
                # Don't retry auth errors
                err_str = str(exc).lower()
                if "auth" in err_str or "key" in err_str:
                    raise
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
        raise RuntimeError(f"LLM call failed after {self.max_retries} attempts: {last_error}")

    def _send_groq(
        self,
        messages: List[Dict[str, Any]],
        system: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        groq_messages: List[Dict[str, Any]] = []
        if system:
            groq_messages.append({"role": "system", "content": system})

        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")

            if isinstance(content, str):
                groq_messages.append({"role": role, "content": content})
            elif isinstance(content, list):
                # Check if it's tool result blocks
                tool_results = [
                    item for item in content
                    if isinstance(item, dict) and item.get("type") == "tool_result"
                ]
                if tool_results:
                    for tr in tool_results:
                        groq_messages.append({
                            "role": "tool",
                            "tool_call_id": tr.get("tool_use_id"),
                            "content": str(tr.get("content", "")),
                        })
                else:
                    # List of blocks from assistant
                    text_parts = []
                    tool_calls = []
                    for b in content:
                        b_type = getattr(b, "type", None) or (b.get("type") if isinstance(b, dict) else None)
                        if b_type == "text":
                            txt = getattr(b, "text", "") if hasattr(b, "text") else b.get("text", "")
                            if txt:
                                text_parts.append(txt)
                        elif b_type == "tool_use":
                            b_id = getattr(b, "id", None) or b.get("id")
                            b_name = getattr(b, "name", None) or b.get("name")
                            b_input = getattr(b, "input", {}) if hasattr(b, "input") else b.get("input", {})
                            tool_calls.append({
                                "id": b_id,
                                "type": "function",
                                "function": {
                                    "name": b_name,
                                    "arguments": json.dumps(b_input) if isinstance(b_input, dict) else str(b_input),
                                },
                            })
                    asst_msg: Dict[str, Any] = {"role": "assistant"}
                    asst_msg["content"] = " ".join(text_parts) if text_parts else None
                    if tool_calls:
                        asst_msg["tool_calls"] = tool_calls
                    groq_messages.append(asst_msg)
            else:
                groq_messages.append({"role": role, "content": str(content)})

        groq_tools = None
        if tools:
            groq_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t["name"],
                        "description": t.get("description", ""),
                        "parameters": t.get("input_schema", {}),
                    },
                }
                for t in tools
            ]

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": groq_messages,
            "max_tokens": self.max_tokens,
        }
        if groq_tools:
            kwargs["tools"] = groq_tools

        completion = self._client.chat.completions.create(**kwargs)
        choice = completion.choices[0]
        msg = choice.message

        blocks = []
        text_content = msg.content
        if not text_content and getattr(msg, "reasoning", None):
            text_content = msg.reasoning

        if text_content:
            blocks.append(TextBlock(text=text_content))

        if getattr(msg, "tool_calls", None):
            for tc in msg.tool_calls:
                try:
                    inp = json.loads(tc.function.arguments) if tc.function.arguments else {}
                except Exception:
                    inp = {"raw": tc.function.arguments}
                blocks.append(ToolUseBlock(
                    id=tc.id,
                    name=tc.function.name,
                    input=inp,
                ))

        return LLMResponse(content=blocks)

    def _send_anthropic(
        self,
        messages: List[Dict[str, Any]],
        system: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        kwargs: Dict[str, Any] = dict(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages,
        )
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = tools
        resp = self._client.messages.create(**kwargs)
        blocks = []
        for b in resp.content:
            if b.type == "text":
                blocks.append(TextBlock(text=b.text))
            elif b.type == "tool_use":
                blocks.append(ToolUseBlock(id=b.id, name=b.name, input=b.input))
        return LLMResponse(content=blocks)

    @staticmethod
    def text_of(message: Any) -> str:
        """Concatenate all text blocks in a response into one string."""
        if hasattr(message, "content"):
            return "".join(b.text for b in message.content if getattr(b, "type", None) == "text")
        return ""
