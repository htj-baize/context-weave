from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextWeaveError(Exception):
    code: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    retryable: bool = False

    def to_payload(self) -> dict[str, Any]:
        return {
            "status": "error",
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
                "retryable": self.retryable,
            },
        }


class InvalidArgumentError(ContextWeaveError):
    def __init__(self, message: str, **details: Any) -> None:
        super().__init__("invalid_argument", message, details)


class NotFoundError(ContextWeaveError):
    def __init__(self, message: str, **details: Any) -> None:
        super().__init__("not_found", message, details)


class ValidationError(ContextWeaveError):
    def __init__(self, message: str, **details: Any) -> None:
        super().__init__("validation_error", message, details)


class ContractError(ContextWeaveError):
    def __init__(self, message: str, **details: Any) -> None:
        super().__init__("contract_error", message, details)


class InternalError(ContextWeaveError):
    def __init__(self, message: str = "internal error", **details: Any) -> None:
        super().__init__("internal_error", message, details)
