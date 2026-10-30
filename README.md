# Ironhaven

An original, Torn-inspired multiplayer city RPG foundation. Ironhaven uses a gritty, compact city-dashboard aesthetic while keeping its own name, fictional world, content, and visual identity.

## Current status

- [x] Dark city-game frontend foundation
- [x] FastAPI backend foundation
- [x] PostgreSQL Docker Compose configuration
- [x] Player registration and login API
- [x] Argon2 password hashing
- [x] Signed, expiring access tokens
- [x] Authenticated player profile endpoint
- [x] Health endpoint
- [x] Connect browser registration and sign-in to the API
- [x] Load authenticated server-side player profiles in the browser
- [x] Serve the browser client and API from one origin
- [ ] Add database migrations, rate limiting, and account recovery
- [ ] Add shared multiplayer features (presence, messaging, rankings, trading)
- [ ] Production deployment and security review

**Important:** The browser can now register and sign in against the API when served by the FastAPI app. Player account fields are stored in the configured database, but work tasks, missions, rankings, marketplace activity, and other game progress are still demo-only and are not saved server-side. This is a development foundation, not a production-ready public service. Do not use a reused or sensitive password.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Service health |
| POST | `/api/auth/register` | Create a player account |
| POST | `/api/auth/login` | Authenticate a player |
| GET | `/api/players/me` | Get the authenticated player's profile |

Interactive API documentation is available at `/docs` while the API is running.

## Local development with Docker

1. Install Docker Desktop / Docker Engine with the Compose plugin.
2. Copy `.env.example` to `.env`.
3. Generate a random secret: `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
4. Put that value in `SECRET_KEY` in `.env`.
5. Set `POSTGRES_PASSWORD` in `.env` to a strong, unique password using URL-safe characters.
6. Start the services: `docker compose up --build`.
7. Open `http://127.0.0.1:8000/` for the Ironhaven browser client.
8. Open `http://127.0.0.1:8000/docs` for API documentation and check `/api/health`.

The API is bound to localhost by default; PostgreSQL is not published to the host network. Keep `.env` private and never commit it.

The FastAPI service serves `index.html` at `/` and the API under `/api` on the same origin. This avoids a separate browser API URL and CORS setup for the local Docker build.

### Run the API without Docker

Use Python 3.12+, install dependencies with `pip install -r requirements.txt`, set `SECRET_KEY` to a random value of at least 32 characters, and optionally set `DATABASE_URL`. The default local database is SQLite for development convenience. Then run:

```bash
uvicorn app.main:app --reload
```

## Security and production notes

This is a development foundation, not a production-ready public service. Before opening registration to the internet, add request rate limiting and abuse controls, email verification and account recovery, Alembic migrations, structured audit logging, monitoring, backups, HTTPS behind a reverse proxy, secure token lifecycle/refresh or server-side sessions, and a security review. Configure exact trusted CORS origins for the deployed frontend. Never expose the PostgreSQL port publicly.

## Project structure

```
app/
  main.py
  config.py
  database.py
  models.py
  schemas.py
  security.py
  dependencies.py
  routes/
    auth.py
    players.py
index.html
requirements.txt
Dockerfile
docker-compose.yml
.env.example
```
