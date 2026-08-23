"""Shared fixtures. The pipeline context is built once for the whole session."""

from __future__ import annotations

import pytest

from sow.pipeline import build_context


@pytest.fixture(scope="session")
def ctx():
    """Stages 1-7 over the real corpus. No model, no API key."""
    return build_context()


@pytest.fixture(scope="session")
def provs(ctx):
    return ctx.partition.provenance
