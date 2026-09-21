# Phanie Magic Touch

A Django portfolio site for Phanie Magic Touch hair studio.

## Stack

- **Django 6** backend with views, models, and the Django admin
- **Server-rendered templates** (`templates/`) styled with vanilla CSS (`static/css/app.css`)
- **Supabase Storage** for images uploaded via the admin (S3-compatible), with
  local media fallback for development
- **Supabase Postgres** in production, SQLite locally
- Deployed on **Vercel** with zero-config Django + automatic `collectstatic`

## Local development

Requires Python 3.10+.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Set up environment variables (optional for local dev):

```bash
copy .env.example .env        # Windows
```

Run the site:

```bash
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to view the site.

### Admin

```bash
python manage.py createsuperuser
```

The admin lives at http://127.0.0.1:8000/admin/. Manage hairstyles, the
business profile, and published/featured flags there. The homepage reads
content straight from the database.

### Tests

```bash
python manage.py test
```

## Data model

- `BusinessProfile` — single-row store for studio name, hero copy, WhatsApp
  number, address, hours, directions and Instagram URLs.
- `Hairstyle` — the portfolio pieces with title, slug, category, caption, an
  optional local image or external URL, plus `published` and `featured` flags.

The `studio` migrations seed a sample business profile and six sample
hairstyles (external image URLs) so the site is populated out of the box.

## Images uploaded from the admin

Uploads go to **Supabase Storage** when configured, so they are viewable both
locally and in production.

1. In Supabase, create a **public** bucket (e.g. `images`).
2. In **Project Settings → Storage**, generate a new **S3 access key** and copy
   the endpoint and region.
3. Set the S3 variables (see `.env.example`) in your local `.env` and in Vercel:

   - `SUPABASE_S3_BUCKET` — your bucket name
   - `SUPABASE_S3_ENDPOINT` — e.g. `https://<ref>.supabase.co/storage/v1/s3`
   - `SUPABASE_S3_REGION` — region shown on the S3 configuration page
   - `SUPABASE_S3_ACCESS_KEY_ID` / `SUPABASE_S3_SECRET_ACCESS_KEY`
   - `SUPABASE_S3_PUBLIC_URL` — e.g. `https://<ref>.supabase.co/storage/v1/object/public/images`

Without `SUPABASE_S3_BUCKET`, uploads go to local `./media` (development only).

## Deploying to Vercel

Vercel auto-detects Django (`manage.py` + `WSGI_APPLICATION`), runs
`collectstatic` during the build, and serves static files from the CDN.
`vercel.json` sets a build command that runs migrations (`build.py`).

1. Import the GitHub repo in Vercel.
2. Add the following **Environment Variables** (Production + Preview):

   - `DJANGO_SECRET_KEY` — a long random string
   - `DJANGO_DEBUG` — `False`
   - `DJANGO_ALLOWED_HOSTS` — `.vercel.app` (add your custom domain too)
   - `DATABASE_URL` — Supabase Postgres connection string, e.g.
     `postgresql://postgres.<ref>:<password>@aws-0-<region>.pooler.supabase.com:5432/postgres?sslmode=require`
   - The `SUPABASE_S3_*` variables from the section above

3. Deploy. The build runs `python manage.py migrate` against `DATABASE_URL`,
   so tables and sample data are created automatically on first deploy.
4. Create your admin account against the production database:

   ```bash
   vercel pull        # pulls env vars into .env.local
   python manage.py createsuperuser --settings=phanie.settings
   ```

   (Or run `createsuperuser` with the production `DATABASE_URL` exported.)

## Notes

- Vercel's filesystem is ephemeral — never rely on local `media/` or SQLite
  in production. The Postgres + Supabase Storage configuration above is what
  makes admin-uploaded images durable and viewable.
- `python manage.py check --deploy` gives production hardening tips.
- Run `python manage.py collectstatic` locally if you preview static output.