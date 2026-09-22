# FastAPI Posts API

A REST API for users, posts, and post likes. It demonstrates FastAPI routing, Pydantic request/response validation, SQLAlchemy ORM models, PostgreSQL, JWT bearer authentication, Alembic migrations, Docker, and pytest API tests.

When the server is running, FastAPI provides interactive API documentation at [`/docs`](http://localhost:8000/docs) (Swagger UI) and [`/redoc`](http://localhost:8000/redoc) (ReDoc).

## Features

- User registration with unique email addresses and bcrypt-hashed passwords.
- OAuth2 password-form login that returns a signed JWT access token.
- Authenticated post creation and listing; only a post owner may update or delete it.
- Authenticated likes and unlikes, with at most one like per user/post pair.
- Post list and detail responses include vote counts.
- PostgreSQL schema changes are versioned with Alembic.

## How it is implemented

```text
HTTP request
    │
    ▼
FastAPI router (app/routers/)
    ├── Pydantic schema validates input and serializes output
    ├── OAuth2 dependency validates Bearer tokens where required
    └── SQLAlchemy session dependency reads/writes PostgreSQL
```

### Application and routers

`app/main.py` creates the `FastAPI` application, configures CORS middleware, and includes user, authentication, post, and vote routers. Its `GET /` endpoint returns a small root response. Automatic SQLAlchemy table creation is intentionally commented out; manage database structure through Alembic migrations.

| Router | Endpoints | Implementation |
| --- | --- | --- |
| `app/routers/user.py` | `/users` | Creates users, rejects duplicate emails, returns public user fields, and lists a user's posts. |
| `app/routers/auth.py` | `/login` | Accepts `OAuth2PasswordRequestForm` credentials, verifies a bcrypt password hash, and returns a JWT. |
| `app/routers/post.py` | `/posts` | Creates, lists, reads, updates, and deletes posts; SQLAlchemy joins posts to votes to calculate counts. |
| `app/routers/votes.py` | `/votes` | Creates/removes a caller's vote after checking the post and existing vote. |

### Configuration

`app/config.py` uses Pydantic Settings to read and validate these environment variables at startup:

| Variable | Purpose | Local Compose example |
| --- | --- | --- |
| `DATABASE_HOSTNAME` | PostgreSQL host | `postgres` |
| `DATABASE_PORT` | PostgreSQL port | `5432` |
| `DATABASE_NAME` | Database name | `fastapi` |
| `DATABASE_USERNAME` | Database user | `yash` |
| `DATABASE_PASSWORD` | Database password | `yash` |
| `SECRET_KEY` | JWT signing secret | a long random secret |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `30` |

> **Security:** do not commit production passwords or signing keys. Provide unique strong values with your deployment environment or an untracked local `.env` file. The committed Compose values are development examples and must be replaced before deployment.

### Database models and sessions

`app/database.py` builds a SQLAlchemy PostgreSQL engine from settings, creates `SessionLocal`, and exposes the `get_db` generator dependency. FastAPI injects that dependency into handlers; it yields one session for the request and closes it afterward.

`app/models.py` contains the SQLAlchemy table mappings:

| Model/table | Fields and relationships |
| --- | --- |
| `User` / `users` | Integer ID, unique email, hashed password, and creation timestamp. |
| `Post` / `posts` | Title, content, publication flag, creation timestamp, and required `user_id`; `Post.user` loads the author. |
| `Vote` / `votes` | Composite primary key of `user_id` and `post_id`, preventing duplicate likes. The model declares cascading foreign keys to users and posts. |

### Schemas, password hashing, and JWTs

`app/schemas.py` keeps external API data separate from ORM objects. Input models such as `UserCreate`, `UserLogin`, `PostCreate`, and `VoteCreate` validate request content. Response models omit passwords, validate email addresses with `EmailStr`, and use `ConfigDict(from_attributes=True)` so Pydantic can serialize SQLAlchemy objects.

`app/utils.py` configures Passlib with bcrypt. Registration hashes the plain-text password before persistence; login verifies a submitted password against that stored hash.

`app/oauth2.py` uses `python-jose` to create a JWT containing `user_id` and an expiration (`exp`) claim. Its `get_current_user` dependency reads the OAuth2 Bearer token, verifies the JWT, and loads the user from the database. Protected calls need:

```http
Authorization: Bearer <access_token>
```

Post creation and post listing require a token. Update and delete operations also compare the token user's ID to `Post.user_id`, so non-owners receive `403 Forbidden`. Voting requires authentication as well.

### Posts, pagination, and votes

The post-list and post-detail queries outer-join `posts` with `votes`, group by post ID, and count `votes.post_id`. The outer join means posts with zero votes are returned. List responses use the `PostWithVotes` schema, whose JSON shape is `{ "Post": { ... }, "votes": 0 }`.

`GET /posts/` accepts:

- `limit` — maximum results; defaults to `10`.
- `skip` — number of rows to offset; defaults to `0`.
- `search` — title substring filter; defaults to an empty string.

### Migrations

Alembic is configured by `alembic.ini` and `db_migration/env.py`. The migration environment constructs its database URL from the application settings and uses `Base.metadata` for autogeneration. Revision files in `db_migration/versions/` create and evolve posts, users, and votes.

Apply the current schema:

```bash
alembic upgrade head
```

After a model change, generate a migration, inspect it, then apply it:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

## Run the project

### Docker Compose (recommended)

The development Compose file starts an API container and PostgreSQL, exposes the API at port `4000`, and runs Uvicorn with reload enabled.

```bash
docker compose -f docker.compose-dev.yml up --build
```

In another terminal, migrate the database:

```bash
docker compose -f docker.compose-dev.yml exec api alembic upgrade head
```

Browse to [http://localhost:4000/docs](http://localhost:4000/docs). Stop services with:

```bash
docker compose -f docker.compose-dev.yml down
```

Use `down -v` only if you intentionally want to delete the persisted development database volume.

### Python virtual environment

1. Install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Export every variable in the [configuration table](#configuration), using a running PostgreSQL server (typically `DATABASE_HOSTNAME=localhost` outside Docker).
3. Create the target database and apply migrations:

   ```bash
   alembic upgrade head
   ```

4. Start Uvicorn:

   ```bash
   uvicorn app.main:app --reload
   ```

The `Dockerfile` installs `requirements.txt`, copies the project, and runs Uvicorn on port `8000`. `Procfile` provides the equivalent command for process-based deployment platforms.

## API reference

Paths below retain their implemented trailing slashes. Protected routes require the Bearer token unless stated otherwise.

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/` | No | Root response. |
| `POST` | `/users/` | No | Register a user. |
| `GET` | `/users/{id}` | No | Get public user data. |
| `GET` | `/users/{user_id}/posts` | No | List a user's posts. |
| `POST` | `/login` | No | Exchange form credentials for a JWT. |
| `GET` | `/posts/` | Yes | List posts/counts; supports `limit`, `skip`, and `search`. |
| `POST` | `/posts/` | Yes | Create a post owned by the caller. |
| `GET` | `/posts/{id}` | No | Get one post and vote count. |
| `PUT` | `/posts/{id}` | Owner | Replace post fields. |
| `DELETE` | `/posts/{id}` | Owner | Delete a post. |
| `POST` | `/votes/{post_id}` | Yes | Like a post. |
| `DELETE` | `/votes/{post_id}` | Yes | Remove the caller's like. |

Register a user:

```bash
curl -X POST http://localhost:4000/users/ \
  -H 'Content-Type: application/json' \
  -d '{"email":"ada@example.com","password":"correct-horse-battery-staple"}'
```

Log in. The request is form-encoded because the route uses `OAuth2PasswordRequestForm`:

```bash
curl -X POST http://localhost:4000/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=ada@example.com&password=correct-horse-battery-staple'
```

Create a post with the returned token:

```bash
curl -X POST http://localhost:4000/posts/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <access_token>' \
  -d '{"title":"Hello FastAPI","content":"My first post","is_published":true}'
```

## Testing

The pytest suite uses FastAPI's `TestClient` and overrides `get_db` with a test SQLAlchemy session. Fixtures recreate tables for each test and provide users, tokens, and posts. The tests cover registration, login/token claims, post listing, and authorization behavior.

Before testing, make PostgreSQL available using the connection string configured in `tests/conftest.py` (or update that test-only value for your environment), then run:

```bash
pytest
```

## Project layout

```text
app/
├── main.py             # FastAPI app, middleware, and router registration
├── config.py           # Environment-backed settings
├── database.py         # Engine, session factory, request-scoped dependency
├── models.py           # SQLAlchemy mappings
├── schemas.py          # Pydantic validation and response models
├── oauth2.py           # JWT helpers and current-user dependency
├── utils.py            # Password hashing and ORM helper
└── routers/            # User, auth, post, and vote handlers
db_migration/           # Alembic environment and migration history
tests/                  # Pytest fixtures and API tests
Dockerfile              # Container image definition
docker.compose-dev.yml  # Local API + PostgreSQL stack
docker.compose-prod.yml # Production-oriented Compose template
```
