# Lab 5: Multi-container application with Docker Compose

Services: **api** (Flask), **db** (PostgreSQL 15), **redis** (cache), **nginx** (optional reverse proxy).

```
client -> nginx:8080 -> api:5000 -> db (PostgreSQL)
                            \-----> redis (cache)
```

## Features
- 4 services, one command to start everything
- named volumes `postgres_data`, `redis_data`
- `healthcheck` for db, redis and api; `depends_on` with `condition: service_healthy`
- configuration through `.env` (not in Git, template in `.env.example`)
- custom networks `backend` (api, db, redis) and `frontend` (nginx, api); nginx cannot reach the db directly
- `restart: unless-stopped`; api runs as non-root user

## Run
```bash
cp .env.example .env        # edit the values
docker compose up --build -d
docker compose ps
docker compose logs -f
```

## Endpoints (API on http://localhost:5000, also through Nginx on http://localhost:8080)
| Method | Path | Description |
|---|---|---|
| GET | `/` | app info |
| GET | `/health` | health check |
| GET | `/db-test` | PostgreSQL connection check |
| GET | `/cache-test` | Redis connection check |
| POST | `/users` | create a user (JSON `name`, `email`) |
| GET | `/users` | list users from the DB |
| GET | `/users/<id>` | one user: Redis cache first (60 s TTL), then DB |

```bash
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
curl http://localhost:5000/users
curl http://localhost:5000/users/1     # "source": "database"
curl http://localhost:5000/users/1     # "source": "cache"
```

## Debugging
```bash
docker compose logs api
docker compose exec api sh
docker compose build --no-cache
docker compose down -v && docker compose up --build -d   # full reset (deletes data!)
```
