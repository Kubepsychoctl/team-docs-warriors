# Lab 4: Environment variables and configuration

A Flask app that is configured only through environment variables, run in two modes (development / production).

## Files
- `config.py` - reads and validates configuration from env vars
- `app.py` - `/` (non-secret config info) and `/db-test` (PostgreSQL connection check)
- `Dockerfile` - no secrets, no `.env` copied into the image, runs as non-root `appuser`
- `.env.example` - template for the team (committed)
- `.env.development`, `.env.production` - real values, **ignored by Git** (see `.gitignore`)

## Setup
```bash
cp .env.example .env.development      # then fill in real values
```
Example values used for the lab: see the lab handout. Never commit real secrets. Generate a key with:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Run
```bash
docker build -t config-app .

# development (Linux: host.docker.internal needs --add-host)
docker run -d --name dev-postgres -e POSTGRES_USER=devuser -e POSTGRES_PASSWORD=devpassword123 -e POSTGRES_DB=devdb -p 5432:5432 postgres:15-alpine
docker run -d --name config-app-dev --env-file .env.development \
  --add-host host.docker.internal:host-gateway -p 5000:5000 config-app
curl http://localhost:5000/ ; curl http://localhost:5000/db-test

# production-like: custom network instead of the old --link (.env.production: DB_HOST=prod-postgres)
docker network create app-network
docker run -d --name prod-postgres --network app-network \
  -e POSTGRES_USER=produser -e POSTGRES_PASSWORD=prodpass123 -e POSTGRES_DB=proddb postgres:15-alpine
docker run -d --name config-app-prod --network app-network --env-file .env.production -p 5001:5000 config-app
curl http://localhost:5001/
```
Without the required variables the container exits immediately with an error (the app does not start with a missing configuration).
