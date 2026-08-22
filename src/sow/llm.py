"""Model client: structured calls, token accounting, and a mock backend.

Structured output is obtained with ``client.messages.parse(output_format=...)``,
which validates the response against a pydantic model before it reaches the
pipeline. A malformed response fails here rather than three stages later.

Two backends:

* ``live``  -- the Anthropic API. Needs ``ANTHROPIC_API_KEY``.
* ``mock``  -- replays a recorded run from ``tests/fixtures/golden_run``. Needs
  no key, so the quality checks run on a cold clone.

Selected with the ``SOW_LLM`` environment variable; ``live`` is the default.
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

# Claude Opus 5. Override with SOW_MODEL if you want to run the pipeline on a
# different model; the pipeline itself is model-agnostic.
DEFAULT_MODEL = "claude-opus-5"

# USD per million tokens, for the cost line in the run summary.
PRICE_PER_MTOK = {"claude-opus-5": (5.0, 25.0)}


@dataclass
class TokenUsage:
    """Cumulative token counts across a run."""

    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    per_stage: dict[str, dict[str, int]] = field(default_factory=dict)

    def record(self, stage: str, usage: Any) -> None:
        """Accumulate one call's usage, globally and per pipeline stage."""
        inp = int(getattr(usage, "input_tokens", 0) or 0)
        out = int(getattr(usage, "output_tokens", 0) or 0)
        cread = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
        cwrite = int(getattr(usage, "cache_creation_input_tokens", 0) or 0)

        self.calls += 1
        self.input_tokens += inp
        self.output_tokens += out
        self.cache_read_tokens += cread
        self.cache_write_tokens += cwrite

        bucket = self.per_stage.setdefault(
            stage, {"calls": 0, "input_tokens": 0, "output_tokens": 0}
        )
        bucket["calls"] += 1
        bucket["input_tokens"] += inp
        bucket["output_tokens"] += out

    def estimated_cost_usd(self, model: str) -> float | None:
        """Approximate cost, or None for a model with no published price here."""
        price = PRICE_PER_MTOK.get(model)
        if price is None:
            return None
        in_rate, out_rate = price
        return (self.input_tokens / 1e6) * in_rate + (self.output_tokens / 1e6) * out_rate

    def summary(self, model: str) -> str:
        """One-block report of token spend for the run."""
        lines = [
            "TOKEN USAGE",
            "-" * 100,
            f"model              : {model}",
            f"model calls        : {self.calls}",
            f"input tokens       : {self.input_tokens:,}",
            f"output tokens      : {self.output_tokens:,}",
            f"total tokens       : {self.input_tokens + self.output_tokens:,}",
        ]
        if self.cache_read_tokens or self.cache_write_tokens:
            lines.append(
                f"cache read/write   : {self.cache_read_tokens:,} / {self.cache_write_tokens:,}"
            )
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


class LlmClient:
    """Thin wrapper over the Anthropic SDK with usage accounting."""

    def __init__(
        self,
        model: str | None = None,
        backend: str | None = None,
        fixture_dir: Path | None = None,
    ) -> None:
        self.model = model or os.environ.get("SOW_MODEL", DEFAULT_MODEL)
        self.backend = (backend or os.environ.get("SOW_LLM", "live")).lower()
        self.usage = TokenUsage()
        self.fixture_dir = fixture_dir
        self._client: Any = None

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
        """One structured call, validated against ``output_format``.

        Args:
            stage: pipeline stage name, used to attribute token spend.
        """
        if self.backend == "mock":
            return self._parse_mock(stage, system, user, output_format)
        return self._parse_live(stage, system, user, output_format, max_tokens, effort)

    def _parse_live(
        self,
        stage: str,
        system: str,
        user: str,
        output_format: type[T],
        max_tokens: int,
        effort: str,
    ) -> T:
        """Call the Anthropic API and validate the structured response."""
        client = self._live_client()
        try:
            response = client.messages.parse(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
                output_format=output_format,
                thinking={"type": "adaptive"},
                output_config={"effort": effort},
            )
        except Exception as exc:  # surfaced, never swallowed
            raise LlmError(f"{stage}: model call failed: {exc}") from exc

        self.usage.record(stage, response.usage)

        if getattr(response, "stop_reason", None) == "refusal":
            raise LlmError(f"{stage}: model declined the request")

        parsed = getattr(response, "parsed_output", None)
        if parsed is None:
            raise LlmError(f"{stage}: model returned no parseable structured output")
        return parsed

    def _live_client(self) -> Any:
        """Construct the SDK client, failing loudly if no credentials exist."""
        if self._client is not None:
            return self._client
        try:
            import anthropic
        except ImportError as exc:
            raise ConfigError(
                "the 'anthropic' package is required for live runs: pip install -e '.[llm]'"
            ) from exc
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise ConfigError(
                "ANTHROPIC_API_KEY is not set. Set it, or run with SOW_LLM=mock "
                "to replay the committed golden run."
            )
        self._client = anthropic.Anthropic()
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

        key = self.fixture_key(stage, system, user)
        path = self.fixture_dir / f"{key}.json"
        if not path.is_file():
            raise LlmError(
                f"{stage}: no recorded response at {path}. The prompt changed, so the "
                f"golden run is stale -- re-record it with 'sow record'."
            )

        payload = json.loads(path.read_text(encoding="utf-8"))
        self.usage.record(stage, _MockUsage(**payload.get("usage", {})))
        return output_format.model_validate(payload["parsed_output"])

    def record(self, stage: str, system: str, user: str, parsed: BaseModel, usage: Any) -> None:
        """Write one call to the fixture directory for later mock replay."""
        if self.fixture_dir is None:
            raise ConfigError("recording requires a fixture directory")
        self.fixture_dir.mkdir(parents=True, exist_ok=True)
        path = self.fixture_dir / f"{self.fixture_key(stage, system, user)}.json"
        path.write_text(
            json.dumps(
                {
                    "stage": stage,
                    "model": self.model,
                    "usage": {
                        "input_tokens": int(getattr(usage, "input_tokens", 0) or 0),
                        "output_tokens": int(getattr(usage, "output_tokens", 0) or 0),
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
