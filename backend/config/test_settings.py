"""
Test settings for pytest.
Uses SQLite instead of PostGIS for testing without external dependencies.
"""
from .settings import *

# Override database to use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Remove GIS apps that require GDAL
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'django.contrib.gis']

# Use default cache for testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Set a dummy API key for testing
OPENWEATHER_API_KEY = 'test_api_key'
