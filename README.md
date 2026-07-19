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

Architecture

Layered (clean) architecture. Dependencies point inward only: outer layers know about inner ones, never the reverse.

```
src/random_watch/
├── entities/                  # Innermost layer: domain entities, no external dependencies
│   ├── movie/                 #   models.py + value_objects.py per entity
│   ├── tv/
│   └── genre/
├── application/               # Use cases and ports
│   ├── common/errors.py       #   ApplicationError, *NotFoundError
│   └── find_random_video/
│       ├── filter_dto/        #   filter DTOs the application accepts
│       ├── interfaces/        #   gateway Protocols + usecase interfaces
│       └── usecases/
├── adapter/tmdb/              # Outgoing side: TMDB gateway
│   ├── models/                #   raw TMDB response models
│   ├── tmdb_client.py         #   HTTP client (aiohttp), returns raw models
│   ├── tmdb_gateway.py        #   implements gateway ports, maps models -> entities
│   └── params.py              #   filter DTO -> TMDB query params mapping
├── infrastructure/            # Incoming side and technical details
│   ├── api/                   #   FastAPI routers, request/response models,
│   │                          #   exception handlers, rate-limit middleware
│   └── config.py              #   pydantic-settings Config
├── dependency_injection.py    # DI container
├── bootstrap.py               # Composition root: setup_* functions, app factory, lifespan
└── __main__.py                # Entry point
```

Key points
- Use cases depend on narrow gateway `Protocol`s (`MovieGateway`, `TvGateway`, `GenreGateway`), not on TMDB. All TMDB specifics (query param names, raw response models) live behind `adapter/tmdb/`.
- Empty search results raise application-level `*NotFoundError`s, mapped to HTTP 404 by exception handlers.
- `bootstrap.py` assembles everything: config, DI container (with wiring), routes, middlewares, exception handlers. The lifespan hook closes the shared HTTP session on shutdown.

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
uv run python -m random_watch
```

Open the interactive docs: http://localhost:8000/docs

Endpoints
- `GET /health` — health check
- `GET /genres/movie` — movie genres
- `GET /genres/tv` — TV genres
- `POST /random/movie` — random movie by filters (404 if nothing matches)
- `POST /random/tv` — random TV show by filters (404 if nothing matches)
- `POST /random/any` — mixed random collection of movies and TV shows

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
uv run pytest -q
```
The API test assembles the real app, so `TMDB_ACCESS_TOKEN` must be set (any value works — no real requests are made).

Contributing
- Open pull requests with clear descriptions and test coverage where appropriate.
- For local development, use a test TMDB key and run the app with `uv run`.

License
- Apache-2.0
