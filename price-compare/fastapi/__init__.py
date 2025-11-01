"""Minimal FastAPI-compatible facade for offline use."""
from .app import Depends, FastAPI, Form, HTTPException, Request
from .responses import HTMLResponse, JSONResponse

__all__ = ["FastAPI", "Request", "Depends", "Form", "HTTPException", "HTMLResponse", "JSONResponse"]
