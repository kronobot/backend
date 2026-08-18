# kronobot-backend

Backend for Kronobot: a Django app that powers the Kronobot website and admin, tracking motorsport events (rally, hill-climb, autocross, karting) and their participants.

## Stack

- Django 5.2, PostgreSQL 16
- django-unfold (admin theme), Sentry, Google Cloud Secret Manager + Cloud Storage in production
- Deployed to Google App Engine Standard (free tier) via GitHub Actions

## Project structure

```
app/            # Django project (manage.py, config/, inventory/)
Dockerfile
docker-compose.yml
Makefile
plans/          # spec-driven development plan files
```

## Local development

Requires Docker and Docker Compose.

```bash
make run              # build and start the app + Postgres containers
```

Once the stack is up, in another terminal:

```bash
make createmigrations # generate new migrations after model changes
make migrate           # apply migrations
make createsuperuser   # create an admin user
```

The app is served at [http://localhost:8000](http://localhost:8000), and the admin at [http://localhost:8000/admin/](http://localhost:8000/admin/).

## Plans

Work is planned before it's implemented. See [plans/](plans/) for task specs, and [plans/_TEMPLATE.md](plans/_TEMPLATE.md) for the format — see [CLAUDE.md](CLAUDE.md) for the full workflow.

## Deployment

Pushes to `main` trigger `.github/workflows/deploy.yaml`, which runs migrations and deploys `app/app.yaml` to App Engine Standard. See [plans/1_initialize-app.md](plans/1_initialize-app.md) for the full setup and known discussion points around the deploy config.
