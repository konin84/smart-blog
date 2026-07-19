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
