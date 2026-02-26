import os
import sys
import django

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables before importing Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

# Try to set defaults for required env vars
if 'USE_DOCKER' not in os.environ:
    os.environ['USE_DOCKER'] = 'no'
if 'DATABASE_URL' not in os.environ:
    os.environ['DATABASE_URL'] = 'sqlite:///db.sqlite3'

django.setup()

from curtaincall.users.models import User

email = "tsvete.pete@gmail.com"
password = "556689tin"

try:
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"✓ Updated existing user {email} to superuser")
    else:
        user = User.objects.create_superuser(email=email, password=password)
        print(f"✓ Created superuser: {email}")
    
    print("✓ Superuser is ready!")
    print(f"  Email: {email}")
    print(f"  Login at: http://localhost:8000/admin")
except Exception as e:
    print(f"Error: {e}")
    print("\nAlternative: Use Django shell:")
    print("  python manage.py shell")
    print("  Then paste:")
    print("  from curtaincall.users.models import User")
    print("  User.objects.create_superuser(email='tsvete.pete@gmail.com', password='556689tin')")

