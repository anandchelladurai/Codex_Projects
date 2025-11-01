"""Simple in-process test client."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from ..app import Request, run_endpoint


@dataclass
class Response:
    status_code: int
    text: str


class TestClient:
    def __init__(self, app) -> None:  # noqa: ANN001 - compatibility
        self.app = app

    def get(self, path: str, headers: Dict[str, str] | None = None) -> Response:
        endpoint = self._resolve(path, "GET")
        request = Request(method="GET", url=path, headers=headers or {}, form_data={})
        result = run_endpoint(endpoint, request)
        return self._normalize(result)

    def post(self, path: str, data: Dict[str, str] | None = None, headers: Dict[str, str] | None = None) -> Response:
        endpoint = self._resolve(path, "POST")
        request = Request(method="POST", url=path, headers=headers or {}, form_data=data or {})
        result = run_endpoint(endpoint, request)
        return self._normalize(result)

    def _resolve(self, path: str, method: str):
        routes = self.app.routes.get(path)
        if not routes or method.upper() not in routes:
            raise ValueError(f"Route {method} {path} not defined")
        return routes[method.upper()]

    @staticmethod
    def _normalize(result) -> Response:  # noqa: ANN001
        if hasattr(result, "status_code") and hasattr(result, "text"):
            return Response(status_code=result.status_code, text=result.text)
        if isinstance(result, str):
            return Response(status_code=200, text=result)
        return Response(status_code=200, text=str(result))

