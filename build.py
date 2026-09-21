"""Vercel build command for the Django app.

Runs database migrations against the production database during each deploy.
Static files are collected automatically by Vercel (see STATIC_ROOT).
"""

import os
import subprocess
import sys


def main():
    if not os.getenv("DATABASE_URL"):
        print("DATABASE_URL not set during build; skipping migrate.")
        return
    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)


if __name__ == "__main__":
    main()