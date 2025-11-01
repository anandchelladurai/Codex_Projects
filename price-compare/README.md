# UK Supermarket Price Compare (Indian Groceries)

This project provides a FastAPI-style web application for comparing prices of Indian grocery items across leading UK supermarkets. The repository ships with a lightweight in-repo compatibility layer so it can run in fully offline environments, while still mirroring FastAPI idioms. When running on a workstation with internet access you can install real dependencies (see below) to swap in the official frameworks transparently. The application defaults to using bundled mock fixtures to deliver instant results without issuing live web requests. Live mode can be enabled via configuration for supported providers.

## Features

- Search interface for Indian grocery products backed by HTMX-powered partial updates.
- Provider/adaptor pattern for supermarket integrations with mock fixtures for immediate use.
- Pack size normalization and unit price calculations with support for metric weight, volume, and item counts.
- Configurable caching, rate limiting, and polite request headers.
- Graceful error handling with warnings surfaced to the UI.
- Comprehensive automated tests covering unit parsing, normalization, provider contracts, and end-to-end flow.

## Getting Started

### Prerequisites

- Python 3.10+
- Recommended: virtual environment (``python -m venv .venv``)

### Installation

```bash
cd price-compare
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # optional when using the built-in offline compatibility layer
cp .env.example .env
```

> **Note:** If you install the official FastAPI/Jinja2/httpx stack the in-repo `fastapi/` shim is no longer required. You can safely delete the `price-compare/fastapi` directory to defer to the upstream packages.

### Configuration

Configuration is driven by environment variables defined in `.env` (loaded automatically via `python-dotenv`). Key settings include:

- `LIVE_MODE`: Enable live scraping (default `false`).
- `REQUEST_TIMEOUT`: Default HTTP timeout for provider requests (seconds).
- `RATE_LIMIT_QPS`: Global per-provider requests per second ceiling.
- `CACHE_TTL_SECONDS`: TTL for in-memory search result cache.
- `HEADLESS`: Whether to run browser-based scrapers headless (reserved for future Playwright integrations).

### Running the App

```bash
uvicorn app.main:app --reload
```

The app will be available at `http://127.0.0.1:8000`. Search for Indian grocery items and compare supermarket prices. Toggle "Use live data" to attempt live fetching where available (mock mode by default).

### Running Tests

```bash
pytest
```

### Docker

A basic Docker setup is provided:

```bash
docker compose up --build
```

### Adding a New Provider

1. Create a new module in `app/providers/` implementing `BaseProvider`.
2. Supply fixture data in `app/providers/fixtures/` (see existing JSON fixtures for format).
3. Register the provider in `app/providers/__init__.py`.
4. Update tests if necessary.

### Notes on Live Scraping

Live scraping is disabled by default. Enabling it may violate terms of service for some retailers; proceed responsibly. The existing integrations use simple HTTP GET requests with polite rate limiting and user-agent headers. Consider expanding integrations with official APIs or consented access where available.

## License

This project is provided for educational purposes.

