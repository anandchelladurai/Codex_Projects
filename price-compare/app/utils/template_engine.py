"""Minimal template engine supporting a Jinja-like syntax subset."""
from __future__ import annotations

from pathlib import Path
from typing import Dict
import re


class TemplateError(Exception):
    """Raised when a template fails to compile."""


class TemplateEngine:
    """Lightweight template renderer for this project."""

    def __init__(self, directory: str) -> None:
        self.directory = Path(directory)
        self._cache: Dict[str, str] = {}

    def render(self, name: str, context: Dict[str, object]) -> str:
        template = self._load_template(name)
        code = self._cache.get(name)
        if code is None:
            code = self._compile(template)
            self._cache[name] = code
        namespace: Dict[str, object] = {
            "__builtins__": {
                "len": len,
                "str": str,
                "min": min,
                "max": max,
                "enumerate": enumerate,
                "range": range,
            }
        }
        namespace.update(context)
        exec(code, namespace)  # noqa: S102 - controlled input
        return namespace["__rendered__"]

    def _load_template(self, name: str) -> str:
        path = self.directory / name
        if not path.exists():
            raise TemplateError(f"Template {name} not found")
        return path.read_text()

    def _compile(self, template: str) -> str:
        token_re = re.compile(r"({{.*?}}|{%.*?%})", re.S)
        tokens = token_re.split(template)
        indent = 1
        code_lines = ["def __render():", "    output = []", "    write = output.append"]

        def add_line(line: str, adjust: int = 0) -> None:
            nonlocal indent
            indent += adjust
            code_lines.append("    " * indent + line)

        for token in tokens:
            if not token:
                continue
            if token.startswith("{{") and token.endswith("}}"): 
                expr = token[2:-2].strip()
                add_line(f"write(str({expr}))")
            elif token.startswith("{%") and token.endswith("%}"):
                statement = token[2:-2].strip()
                if statement.startswith("if "):
                    add_line(f"if {statement[3:].strip()}:", adjust=0)
                    indent += 1
                elif statement.startswith("elif "):
                    indent -= 1
                    add_line(f"elif {statement[5:].strip()}:", adjust=0)
                    indent += 1
                elif statement == "else":
                    indent -= 1
                    add_line("else:")
                    indent += 1
                elif statement == "endif":
                    indent -= 1
                elif statement.startswith("for ") and " in " in statement:
                    add_line(f"for {statement[4:].strip()}:", adjust=0)
                    indent += 1
                elif statement == "endfor":
                    indent -= 1
                elif statement.startswith("set ") and "=" in statement:
                    add_line(statement[4:].strip())
                else:
                    raise TemplateError(f"Unsupported statement: {statement}")
            else:
                add_line(f"write({token!r})")
        code_lines.append("    return ''.join(output)")
        code_lines.append("__rendered__ = __render()")
        return "\n".join(code_lines)


__all__ = ["TemplateEngine", "TemplateError"]

