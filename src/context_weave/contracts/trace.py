from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .context import ContextTrace


def serialize_context_trace(trace: ContextTrace) -> dict[str, Any]:
    return asdict(trace)

