"""
HireMind AI — Django backend settings.
Minimal on purpose: no DB (in-memory store), no CSRF (pure JSON API served
to our own React app), same API contract as the FastAPI version.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "hiremind-hackathon-demo-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]   # preview proxies use random hosts

INSTALLED_APPS = []     # no ORM models needed — agents are pure Python

MIDDLEWARE = []         # no SecurityMiddleware => no X-Frame-Options (preview iframe ok)

ROOT_URLCONF = "hiremind.urls"
WSGI_APPLICATION = "hiremind.wsgi.application"

DATABASES = {}          # in-memory store only

LANGUAGE_CODE = "en-us"
USE_TZ = True
