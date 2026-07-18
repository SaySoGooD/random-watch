# random-watch

REST API for discovering random movies and TV shows via the [TMDB](https://www.themoviedb.org/) API.

**Live:** https://api.saysogood.dev/docs

---

## Stack

- **Python 3.14** / **FastAPI** / **uvicorn**
- **aiohttp** — async HTTP client for TMDB
- **pydantic-settings** — config from `.env`
- **dependency-injector** — DI container
- **slowapi** — per-client rate limiting

---

## Project structure

```
src/
├── adapter/tmdb/          # TMDB API adapter + response models
├── application/           # Use cases, interfaces, DTOs
│   └── find_random_video/
│       ├── filter_dto/
│       ├── result_dto/
│       ├── interfaces/
│       └── usecases/
├── infrastructure/
│   ├── api/               # FastAPI app, routers, middleware
│   │   ├── __init__.py    # App factory, exception handlers, rate limiting
│   │   ├── routers.py
│   │   └── ratelimit_middleware.py
│   └── models/            # Pydantic request/response models
│       ├── base.py
│       ├── movie.py
│       ├── tv.py
│       ├── any.py
│       ├── genre.py
│       └── enums.py
└── main/
    ├── config.py           # Pydantic settings
    └── dependency_injection.py
```

---

## Getting started

### Requirements

- Python 3.14+
- [uv](https://github.com/astral-sh/uv)
- TMDB API access token — get one at https://www.themoviedb.org/settings/api

### Install

```bash
git clone https://github.com/SaySoGooD/random-watch.git
cd random-watch
uv sync
```

### Configure

```bash
cp .env.example .env
```

`.env`:

```env
TMDB_ACCESS_TOKEN=your_token_here

# Optional (defaults shown)
API_HOST=0.0.0.0
API_PORT=8000
API_RATE_LIMIT_PER_CLIENT=35
API_RATE_LIMIT_GLOBAL=35
API_RATE_LIMIT_WINDOW=10
```

### Run

```bash
uv run python -m src
```

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness probe |
| `GET` | `/genres/movie` | All available movie genres |
| `GET` | `/genres/tv` | All available TV show genres |
| `POST` | `/random/movie` | Random movie by filters |
| `POST` | `/random/tv` | Random TV show by filters |
| `POST` | `/random/any` | Mixed random collection |

Full interactive docs: `/docs`

### Example

```bash
curl -X POST https://api.saysogood.dev/random/movie \
  -H "Content-Type: application/json" \
  -d '{
    "vote_average_gte": 7.5,
    "vote_count_gte": 1000,
    "with_genres": "28",
    "sort_by": "popularity.desc"
  }'
```

---

## Rate limiting

- **Per client:** 35 requests / 10 seconds
- **Global:** 35 requests / 10 seconds across all clients

Both limits return `429` when exceeded.
