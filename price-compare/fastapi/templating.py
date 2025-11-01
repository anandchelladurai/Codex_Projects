"""Template helper using the local template engine."""
from __future__ import annotations

from typing import Dict

from .responses import HTMLResponse
from app.utils.template_engine import TemplateEngine


class Jinja2Templates:
    def __init__(self, directory: str) -> None:
        self.engine = TemplateEngine(directory)

    def TemplateResponse(self, name: str, context: Dict[str, object], status_code: int = 200) -> HTMLResponse:
        content = self.engine.render(name, context)
        return HTMLResponse(content=content, status_code=status_code)

