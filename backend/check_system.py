import os
import sys
import django
from django.conf import settings

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def check_system():
    print("🔍 Starting Backend Smoke Test...")
    
    # 1. Check Django Import
    try:
        django.setup()
        print("✅ Django imported and setup successfully.")
    except Exception as e:
        print(f"❌ Failed to import/setup Django: {e}")
        sys.exit(1)

    # 2. Check Database Connection
    try:
        from django.db import connections
        from django.db.utils import OperationalError
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
            print("✅ Database connection successful.")
        except OperationalError:
            print("❌ Database connection failed.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Database check failed with error: {e}")
        sys.exit(1)

    # 3. Check Environment Variables
    api_key = os.getenv('OPENWEATHER_API_KEY') or getattr(settings, 'OPENWEATHER_API_KEY', None)
    if api_key:
        print("✅ OPENWEATHER_API_KEY is loaded.")
    else:
        print("❌ OPENWEATHER_API_KEY is missing.")
        sys.exit(1)

    print("\n✅ Backend Healthy")

if __name__ == "__main__":
    check_system()
