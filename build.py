"""Vercel build command for the Django app.

Only production deployments should apply migrations to the configured database.
Preview builds must not mutate a shared production database.
"""
import os
import subprocess
import sys


def main():
    vercel_env = os.getenv("VERCEL_ENV")
    if vercel_env in {"preview", "development"}:
        print(f"Skipping database migrations for Vercel {vercel_env} deployment.")
        return

    if not os.getenv("DATABASE_URL"):
        print("DATABASE_URL not set during build; skipping migrate.")
        return

    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)


if __name__ == "__main__":
    main()
