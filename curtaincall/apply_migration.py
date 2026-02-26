#!/usr/bin/env python
"""Script to apply the role field migration"""
import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.core.management import call_command
from django.db import connection

print("=" * 60)
print("Applying migration to fix role field max_length...")
print("=" * 60)

# Check current database
print(f"\nDatabase: {connection.vendor}")

# Apply migration
try:
    call_command('migrate', 'users', '0003', verbosity=2)
    print("\n✓ Migration applied successfully!")
except Exception as e:
    print(f"\n✗ Error applying migration: {e}")
    print("\nTrying to apply all migrations...")
    try:
        call_command('migrate', verbosity=2)
        print("\n✓ All migrations applied!")
    except Exception as e2:
        print(f"\n✗ Error: {e2}")
        sys.exit(1)

print("\n" + "=" * 60)
print("Migration complete! You can now try registering again.")
print("=" * 60)

