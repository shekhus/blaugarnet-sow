"""Model client: structured calls, token accounting, and a mock backend.

This is the only provider-specific module. Everything downstream consumes
validated pydantic models and never sees a provider type, so support for a
second API costs one method here and nothing anywhere else.

Two providers, chosen by whichever key is present (or forced with
``SOW_PROVIDER``):

* ``anthropic`` -- ``ANTHROPIC_API_KEY``, via ``messages.parse``
* ``openai``    -- ``OPENAI_API_KEY``, via ``chat.completions.parse``

Two backends, chosen with ``SOW_LLM``:

* ``live`` -- call the API. Default.
* ``mock`` -- replay a recorded run from ``tests/fixtures/golden_run``. Needs no
  key, so the quality checks run on a cold clone.

Structured output is validated against a pydantic model before it reaches the
pipeline, so a malformed response fails here rather than three stages later.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel

from .config import ConfigError

T = TypeVar("T", bound=BaseModel)

PROVIDER_KEY_ENV = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"}
DEFAULT_MODEL = {"anthropic": "claude-opus-5", "openai": "gpt-5.4"}

# USD per million tokens (input, output). Absent entries omit the cost line
# rather than reporting a guess.
PRICE_PER_MTOK: dict[str, tuple[float, float]] = {"claude-opus-5": (5.0, 25.0)}


def detect_provider() -> str:
    """Pick a provider from SOW_PROVIDER, or from whichever key is present."""
    forced = os.environ.get("SOW_PROVIDER", "").strip().lower()
    if forced:
        if forced not in PROVIDER_KEY_ENV:
            raise ConfigError(
                f"SOW_PROVIDER must be one of {sorted(PROVIDER_KEY_ENV)}, got '{forced}'"
            )
        return forced
    for provider, env_var in PROVIDER_KEY_ENV.items():
        if os.environ.get(env_var):
            return provider
    return "anthropic"


@dataclass
class TokenUsage:
    """Cumulative token counts across a run, provider-independent."""

    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    last: tuple[int, int] = (0, 0)
    per_stage: dict[str, dict[str, int]] = field(default_factory=dict)

    def record(self, stage: str, usage: Any) -> None:
        """Accumulate one call's usage.

        Reads whichever field names the provider used: Anthropic reports
        input_tokens/output_tokens, OpenAI prompt_tokens/completion_tokens.
        """

        def pick(*names: str) -> int:
            for name in names:
                value = getattr(usage, name, None)
                if value:
                    return int(value)
            return 0

        inp = pick("input_tokens", "prompt_tokens")
        out = pick("output_tokens", "completion_tokens")
        cached = pick("cache_read_input_tokens")
        self.last = (inp, out)

        self.calls += 1
        self.input_tokens += inp
        self.output_tokens += out
        self.cached_tokens += cached

        bucket = self.per_stage.setdefault(
            stage, {"calls": 0, "input_tokens": 0, "output_tokens": 0}
        )
        bucket["calls"] += 1
        bucket["input_tokens"] += inp
        bucket["output_tokens"] += out

    def estimated_cost_usd(self, model: str) -> float | None:
        """Approximate cost, or None for a model with no price recorded here."""
        price = PRICE_PER_MTOK.get(model)
        if price is None:
            return None
        in_rate, out_rate = price
        return (self.input_tokens / 1e6) * in_rate + (self.output_tokens / 1e6) * out_rate

    def summary(self, model: str, provider: str = "") -> str:
        """One-block report of token spend for the run."""
        lines = [
            "TOKEN USAGE",
            "-" * 100,
            f"provider           : {provider or 'n/a'}",
            f"model              : {model}",
            f"model calls        : {self.calls}",
            f"input tokens       : {self.input_tokens:,}",
            f"output tokens      : {self.output_tokens:,}",
            f"total tokens       : {self.input_tokens + self.output_tokens:,}",
        ]
        if self.cached_tokens:
            lines.append(f"  of which cached  : {self.cached_tokens:,}")
        for stage, bucket in sorted(self.per_stage.items()):
            lines.append(
                f"  {stage:<17}: {bucket['calls']} call(s), "
                f"{bucket['input_tokens']:,} in / {bucket['output_tokens']:,} out"
            )
        cost = self.estimated_cost_usd(model)
        if cost is not None:
            lines.append(f"estimated cost     : USD {cost:.4f}")
        lines.append("-" * 100)
        return "\n".join(lines)


class LlmError(RuntimeError):
    """Raised when the model cannot be reached or its response is unusable."""


def _key_source_hint(provider: str, exc: Exception) -> str:
    """On an auth or quota failure, say which key was used and where it came from."""
    text = str(exc).lower()
    if not any(m in text for m in ("authentication", "401", "quota", "429", "billing")):
        return ""

    from .config import ENV_PATH

    env_var = PROVIDER_KEY_ENV[provider]
    key = os.environ.get(env_var, "")
    if not key:
        return f"\n  hint: {env_var} is not set."

    fingerprint = f"{key[:11]}...{key[-4:]}" if len(key) > 18 else "(short value)"
    hint = f"\n  hint: used {env_var} = {fingerprint} ({len(key)} chars)"
    hint += f", loaded from {ENV_PATH.name}." if ENV_PATH.is_file() else " from the environment."
    if "quota" in text or "billing" in text:
        hint += "\n        The key is valid but the account has no credit."
    return hint


class LlmClient:
    """Thin wrapper over a provider SDK, with usage accounting."""

    def __init__(
        self,
        model: str | None = None,
        backend: str | None = None,
        provider: str | None = None,
        fixture_dir: Path | None = None,
        record_fixtures: bool = False,
    ) -> None:
        self.provider = provider or detect_provider()
        self.model = model or os.environ.get("SOW_MODEL") or DEFAULT_MODEL[self.provider]
        self.backend = (backend or os.environ.get("SOW_LLM", "live")).lower()
        self.usage = TokenUsage()
        self.fixture_dir = fixture_dir
        self.record_fixtures = record_fixtures
        self._client: Any = None
        self._last_usage: tuple[int, int] = (0, 0)

        if self.backend not in ("live", "mock"):
            raise ConfigError(f"SOW_LLM must be 'live' or 'mock', got '{self.backend}'")

    def parse(
        self,
        stage: str,
        system: str,
        user: str,
        output_format: type[T],
        max_tokens: int = 16000,
        effort: str = "high",
    ) -> T:
        """One structured call, validated against ``output_format``."""
        if self.backend == "mock":
            return self._parse_mock(stage, system, user, output_format)

        client = self._live_client()
        try:
            if self.provider == "anthropic":
                parsed = self._parse_anthropic(
                    client, stage, system, user, output_format, max_tokens, effort
                )
            else:
                parsed = self._parse_openai(
                    client, stage, system, user, output_format, max_tokens, effort
                )
            if self.record_fixtures:
                self.record(stage, system, user, parsed)
            return parsed
        except LlmError:
            raise
        except Exception as exc:  # surfaced, never swallowed
            raise LlmError(
                f"{stage}: model call failed: {exc}{_key_source_hint(self.provider, exc)}"
            ) from exc

    def _parse_anthropic(
        self, client, stage, system, user, output_format, max_tokens, effort
    ) -> Any:
        """Anthropic Messages API with adaptive thinking and structured output."""
        response = client.messages.parse(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
            output_format=output_format,
            thinking={"type": "adaptive"},
            output_config={"effort": effort},
        )
        self.usage.record(stage, response.usage)

        if getattr(response, "stop_reason", None) == "refusal":
            details = getattr(response, "stop_details", None)
            reason = getattr(details, "explanation", "") if details else ""
            raise LlmError(f"{stage}: model declined the request. {reason}")

        parsed = getattr(response, "parsed_output", None)
        if parsed is None:
            raise LlmError(
                f"{stage}: no parseable structured output "
                f"(stop_reason={getattr(response, 'stop_reason', '?')}). "
                f"If this is 'max_tokens', raise max_tokens."
            )
        return parsed

    def _parse_openai(
        self, client, stage, system, user, output_format, max_tokens, effort
    ) -> Any:
        """OpenAI chat completions with structured output."""
        request: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": output_format,
            "max_completion_tokens": max_tokens,
        }
        if effort:
            request["reasoning_effort"] = effort

        response = client.chat.completions.parse(**request)
        self.usage.record(stage, response.usage)

        message = response.choices[0].message
        if getattr(message, "refusal", None):
            raise LlmError(f"{stage}: model declined the request: {message.refusal}")

        parsed = getattr(message, "parsed", None)
        if parsed is None:
            finish = getattr(response.choices[0], "finish_reason", "unknown")
            raise LlmError(
                f"{stage}: no parseable structured output (finish_reason={finish}). "
                f"If this is 'length', raise max_completion_tokens."
            )
        return parsed

    def _live_client(self) -> Any:
        """Construct the provider SDK client, failing loudly without credentials."""
        if self._client is not None:
            return self._client

        env_var = PROVIDER_KEY_ENV[self.provider]
        if not os.environ.get(env_var):
            raise ConfigError(
                f"{env_var} is not set. Put it in .env (see .env.example), export it, "
                f"or run with SOW_LLM=mock to replay the committed golden run."
            )

        if self.provider == "anthropic":
            try:
                import anthropic
            except ImportError as exc:
                raise ConfigError(
                    "the 'anthropic' package is required: pip install -e '.[llm]'"
                ) from exc
            self._client = anthropic.Anthropic()
        else:
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise ConfigError(
                    "the 'openai' package is required: pip install -e '.[openai]'"
                ) from exc
            self._client = OpenAI()
        return self._client

    # ---------------------------------------------------------------- mock --

    @staticmethod
    def fixture_key(stage: str, system: str, user: str) -> str:
        """Stable key for a recorded call: stage plus a hash of the exact prompt."""
        digest = hashlib.sha256(f"{system}\x00{user}".encode("utf-8")).hexdigest()[:16]
        return f"{stage}-{digest}"

    def _parse_mock(self, stage: str, system: str, user: str, output_format: type[T]) -> T:
        """Replay a recorded response for this exact prompt.

        A missing recording is an error, never a silent fall-through to a live
        call: a mock run that quietly reached the network would invalidate every
        offline guarantee the tests rely on.
        """
        if self.fixture_dir is None:
            raise ConfigError("mock backend requires a fixture directory")

        path = self.fixture_dir / f"{self.fixture_key(stage, system, user)}.json"
        if not path.is_file():
            raise LlmError(
                f"{stage}: no recorded response at {path}. The prompt changed, so the "
                f"golden run is stale -- re-record it with 'sow draft --record'."
            )

        payload = json.loads(path.read_text(encoding="utf-8"))
        self.usage.record(stage, _MockUsage(**payload.get("usage", {})))
        return output_format.model_validate(payload["parsed_output"])

    def record(self, stage: str, system: str, user: str, parsed: BaseModel) -> None:
        """Write one call to the fixture directory for later mock replay.

        The real token counts are stored alongside the response, so replaying a
        golden run reports what the recorded run actually cost rather than zero.
        """
        if self.fixture_dir is None:
            raise ConfigError("recording requires a fixture directory")
        self.fixture_dir.mkdir(parents=True, exist_ok=True)
        path = self.fixture_dir / f"{self.fixture_key(stage, system, user)}.json"
        path.write_text(
            json.dumps(
                {
                    "stage": stage,
                    "provider": self.provider,
                    "model": self.model,
                    "usage": {
                        "input_tokens": self.usage.last[0],
                        "output_tokens": self.usage.last[1],
                    },
                    "parsed_output": parsed.model_dump(mode="json"),
                },
                indent=2,
            ),
            encoding="utf-8",
        )


@dataclass
class _MockUsage:
    """Usage shape for replayed calls."""

    input_tokens: int = 0
    output_tokens: int = 0
