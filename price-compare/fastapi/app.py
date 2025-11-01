"""Simplified FastAPI-like application for tests."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, Optional


@dataclass
class HTTPException(Exception):
    status_code: int
    detail: str


@dataclass
class Request:
    method: str
    url: str
    headers: Dict[str, str]
    form_data: Dict[str, str]

    async def form(self) -> Dict[str, str]:
        return self.form_data


class Depends:
    def __init__(self, dependency: Callable[..., Any]) -> None:
        self.dependency = dependency


class Form:
    def __init__(self, default: str = "") -> None:
        self.default = default


RouteHandler = Callable[..., Awaitable[Any]] | Callable[..., Any]


class FastAPI:
    """Extremely small subset of FastAPI routing for synchronous tests."""

    def __init__(self, title: str | None = None) -> None:
        self.title = title or "FastAPI"
        self.routes: Dict[str, Dict[str, RouteHandler]] = {}

    def add_api_route(self, path: str, endpoint: RouteHandler, methods: list[str]) -> None:
        self.routes.setdefault(path, {})
        for method in methods:
            self.routes[path][method.upper()] = endpoint

    def get(self, path: str, **_: Any) -> Callable[[RouteHandler], RouteHandler]:
        def decorator(func: RouteHandler) -> RouteHandler:
            self.add_api_route(path, func, ["GET"])
            return func

        return decorator

    def post(self, path: str, **_: Any) -> Callable[[RouteHandler], RouteHandler]:
        def decorator(func: RouteHandler) -> RouteHandler:
            self.add_api_route(path, func, ["POST"])
            return func

        return decorator

    def add_middleware(self, *_: Any, **__: Any) -> None:  # pragma: no cover - noop
        return None


def resolve_dependencies(func: RouteHandler, request: Request) -> Dict[str, Any]:
    from inspect import signature

    sig = signature(func)
    values: Dict[str, Any] = {}
    for name, parameter in sig.parameters.items():
        default = parameter.default
        annotation = parameter.annotation
        if annotation is Request:
            values[name] = request
            continue
        if isinstance(default, Depends):
            dependency = default.dependency
            if asyncio.iscoroutinefunction(dependency):
                values[name] = asyncio.run(dependency())
            else:
                values[name] = dependency()
            continue
        if isinstance(default, Form):
            values[name] = request.form_data.get(name, default.default)
            continue
        values[name] = request.form_data.get(name, default if default is not None else None)
    return values


def run_endpoint(endpoint: RouteHandler, request: Request) -> Any:
    kwargs = resolve_dependencies(endpoint, request)
    if asyncio.iscoroutinefunction(endpoint):
        return asyncio.run(endpoint(**kwargs))
    return endpoint(**kwargs)

