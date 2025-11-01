"""FastAPI application entrypoint."""
from __future__ import annotations

import asyncio
import html
from dataclasses import dataclass
from typing import Dict, List

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .config import Settings, get_settings
from .providers import get_providers
from .providers.base import BaseProvider
from .schemas import ProductResult, SearchRequest, SearchResponse
from .utils.caching import TTLCache, make_cache_key

app = FastAPI(title="UK Supermarket Price Compare")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")
settings = get_settings()
providers_registry = get_providers()
cache = TTLCache(settings.cache_ttl_seconds)

BRAND_KEYWORDS = [
    "tilda",
    "laila",
    "trs",
    "heera",
    "east end",
    "maggi",
    "mdh",
    "aashirvaad",
    "patak",
    "shan",
    "ashoka",
]


@dataclass
class RenderProduct:
    retailer: str
    title: str
    size: str
    total_price_formatted: str
    unit_price_formatted: str
    in_stock: bool
    last_checked_display: str
    url: str
    is_indian_brand: bool


class SearchCoordinator:
    """Coordinates search across providers."""

    def __init__(self, providers: Dict[str, BaseProvider], cache: TTLCache) -> None:
        self.providers = providers
        self.cache = cache

    async def search(self, request: SearchRequest) -> SearchResponse:
        cache_key = make_cache_key(request.query.lower(), str(request.indian_only), request.sort_by)
        cached = None if request.live else self.cache.get(cache_key)
        if cached:
            return cached

        warnings: List[str] = []

        async def run_provider(provider: BaseProvider) -> List[ProductResult]:
            provider.set_warning_callback(warnings.append)
            try:
                return await provider.search(request.query, live=request.live, indian_only=request.indian_only)
            except Exception as exc:  # noqa: BLE001
                warnings.append(f"{provider.retailer}: {exc}")
                return []
            finally:
                provider.set_warning_callback(None)

        tasks = [run_provider(provider) for provider in self.providers.values()]
        results_nested = await asyncio.gather(*tasks)
        results = [item for sub in results_nested for item in sub]

        sorted_results = self.sort_results(results, request.sort_by)
        response = SearchResponse(results=sorted_results, warnings=warnings)
        if not request.live:
            self.cache.set(cache_key, response)
        return response

    @staticmethod
    def sort_results(results: List[ProductResult], sort_by: str) -> List[ProductResult]:
        if sort_by == "total":
            key = lambda product: (product.total_price, product.unit_price)
        else:
            key = lambda product: (product.unit_price, product.total_price)
        return sorted(results, key=key)


async def get_coordinator(_: Settings = Depends(get_settings)) -> SearchCoordinator:
    return SearchCoordinator(providers=providers_registry, cache=cache)


@app.get("/healthz", response_class=JSONResponse)
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/search", response_class=HTMLResponse)
async def search(
    request: Request,
    query: str = Form(""),
    live: str = Form("false"),
    indian_only: str = Form("false"),
    sort_by: str = Form("unit"),
    coordinator: SearchCoordinator = Depends(get_coordinator),
) -> HTMLResponse:
    query_clean = html.escape(query.strip())
    if not query_clean or len(query_clean) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    live_flag = live.lower() == "true"
    indian_flag = indian_only.lower() == "true"
    try:
        request_model = SearchRequest(query=query_clean, live=live_flag, indian_only=indian_flag, sort_by=sort_by)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    response = await coordinator.search(request_model)
    render_results = [
        RenderProduct(
            retailer=item.retailer,
            title=item.title,
            size=item.size,
            total_price_formatted=f"{item.total_price:.2f}",
            unit_price_formatted=f"{item.unit_price:.4f}",
            in_stock=item.in_stock,
            last_checked_display=item.last_checked.strftime("%Y-%m-%d %H:%M UTC"),
            url=str(item.url),
            is_indian_brand=any(keyword in item.title.lower() for keyword in BRAND_KEYWORDS),
        )
        for item in response.results
    ]
    context = {
        "request": request,
        "results": render_results,
        "warnings": response.warnings,
        "sort_by": sort_by,
        "query": query_clean,
        "live": live_flag,
        "indian_only": indian_flag,
    }
    return templates.TemplateResponse("_results.html", context)

