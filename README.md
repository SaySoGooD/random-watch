# random-watch

REST API for discovering random movies and TV shows using the TMDB (The Movie Database) API.

Live API docs are available at `/docs` when the application is running.

Summary
- Exposes endpoints to get a random movie, TV show, or mixed item based on filters.
- Rate-limited (per-client and global) to prevent abuse.

Tech stack
- Python 3.14, FastAPI, uv, aiohttp
- pydantic-settings for configuration
- dependency-injector for dependency management
- slowapi for request rate limiting

Project structure (overview)
```
src/
├── adapter/tmdb/          # TMDB adapter + response models
├── application/           # Use cases, DTOs, interfaces
└── infrastructure/        # FastAPI app, routers, middleware, API models
    └── api/
        ├── __init__.py    # app instance and exception handlers
        └── routers.py
```

Quick start

Requirements
- Python 3.14+
- TMDB API access token: https://www.themoviedb.org/settings/api

Install
```bash
git clone https://github.com/SaySoGooD/random-watch.git
cd random-watch
uv sync
```

Configure
```bash
cp .env.example .env
# Edit .env and set TMDB_ACCESS_TOKEN and other options if needed
```

Example `.env` (defaults in `.env.example`)
```
TMDB_ACCESS_TOKEN=your_token_here
API_HOST=0.0.0.0
API_PORT=8000
API_RATE_LIMIT_PER_CLIENT=35
API_RATE_LIMIT_GLOBAL=35
API_RATE_LIMIT_WINDOW=10
```

Run
```bash
uv run python -m src
```

Open the interactive docs: http://localhost:8000/docs

Endpoints
- `GET /health` — health check
- `GET /genres/movie` — movie genres
- `GET /genres/tv` — TV genres
- `POST /random/movie` — random movie by filters
- `POST /random/tv` — random TV show by filters
- `POST /random/any` — mixed random item

See the Swagger UI for full request/response schemas and examples.

Example request
```bash
curl -X POST http://localhost:8000/random/movie \
  -H "Content-Type: application/json" \
  -d '{
    "vote_average_gte": 7.5,
    "vote_count_gte": 1000,
    "with_genres": "28",
    "sort_by": "popularity.desc"
  }'
```

Rate limiting
- Per-client and global limits configurable via environment variables.
- Exceeding limits returns `429 Too Many Requests`.

Tests
```bash
pytest -q
```

Contributing
- Open pull requests with clear descriptions and test coverage where appropriate.
- For local development, use a test TMDB key and run the app with `uv run`.

License
- MIT

If you want, I can add an "Architecture" section, detailed examples for each endpoint, or translate this back to Russian.
