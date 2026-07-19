# smart-blog

A minimal Django blog backend application.

## What this repo includes

- Django app `blog`
- REST API endpoints for posts, categories, and tags
- RSS feed and sitemap support
- Admin configuration for content management

## Setup

### 1. Install Python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

### 2. Create environment file

```bash
cp .env.example .env
```

### 2.1 Optional: Enable Cloudinary storage

Set `USE_CLOUDINARY=True` in `.env` and fill in the following variables:

```bash
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Create a superuser

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

### Optional: using Rav

If you have `rav` installed, you can run:

```bash
rav install
rav migrate
rav server
```

## Deployment

### Render

For Render, this repository includes `render.yaml` and `Procfile`.

1. Connect this repo to Render
2. Set the environment variables:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=<your-domain>`
   - `DATABASE_URL` (Render Postgres URL or Neon connection string if using Neon)
   - `USE_CLOUDINARY=True` if using Cloudinary
   - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
   - `EMAIL_BACKEND` (for production, for example `anymail.backends.mailgun.EmailBackend` or `anymail.backends.resend.EmailBackend`)
   - `DEFAULT_FROM_EMAIL`
   - `MAILGUN_API_KEY`, `MAILGUN_SENDER_DOMAIN`
   - `RESEND_API_KEY`

   If you use Neon, set `DATABASE_URL` to the full Neon Postgres URL and include `sslmode=require` if required by your Neon connection string.

3. Render will build with `pip install -r requirements.txt`
4. The app starts using `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

### Vercel front-end hosting

This repo is backend-only. When you add a frontend repo, you can deploy it separately on Vercel and point the frontend API calls to the Render backend.

## API Endpoints

- `GET /api/posts/`
- `GET /api/posts/<slug>/`
- `GET /api/categories/`
- `GET /api/tags/`
- `GET /rss/`
- `GET /sitemap.xml`

## Notes

- This repository currently contains only the Django backend.
- No frontend application is included.
