# Repo Overview

- Name: ecom_project
- Stack: Django (REST) + React
- Deploy targets: Render (backend), Netlify (frontend)

## Backend
- Entry: manage.py / ecom_project.wsgi:application
- Python: 3.11.x (Render)
- DB: dj-database-url (Postgres on Render), sqlite local fallback
- Static: WhiteNoise + collectstatic -> staticfiles
- Auth: SimpleJWT
- Storage: Cloudinary (optional)
- CORS: currently CORS_ALLOW_ALL_ORIGINS=True (dev); tighten in prod

## Frontend
- CRA (react-scripts)
- Build: npm run build
- Netlify publish: build/
- API base: REACT_APP_API_URL (should include /api)

## Deploy files
- render.yaml: defines web service + Postgres, gunicorn start
- frontend/netlify.toml: build command and redirects

## Post-deploy steps
- Create admin user via manage.py createsuperuser or helper script
- Set ENV: SECRET_KEY, DATABASE_URL, CLOUDINARY_*, FIREBASE_*