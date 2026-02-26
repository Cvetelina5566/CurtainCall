#!/usr/bin/env python
"""
Script to create a Django superuser.
"""
import os
import sys
import django

# Setup environment variables
os.environ.setdefault("USE_DOCKER", "no")
os.environ.setdefault("DATABASE_URL", "sqlite:///db.sqlite3")

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from curtaincall.users.models import User

def main():
    email = "tsvete.pete@gmail.com"
    password = "Curtain765@"
    
    # Check if user already exists
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"✓ Updated existing user {email} to superuser")
    else:
        # Create new superuser
        user = User.objects.create_superuser(
            email=email,
            password=password
        )
        print(f"✓ Created superuser: {email}")
    
    print("✓ Superuser is ready to use!")
    print(f"  Email: {email}")
    print(f"  You can now log in at: http://localhost:8000/admin")

if __name__ == "__main__":
    main()

