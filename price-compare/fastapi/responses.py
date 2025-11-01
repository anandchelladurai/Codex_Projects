"""Simplified response classes."""
from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass
class HTMLResponse:
    content: str
    status_code: int = 200

    @property
    def text(self) -> str:
        return self.content


@dataclass
class JSONResponse:
    content: dict
    status_code: int = 200

    @property
    def text(self) -> str:
        return json.dumps(self.content)

