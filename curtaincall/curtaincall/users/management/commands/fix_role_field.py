from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fix the role field max_length in the database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if using SQLite
            if 'sqlite' in connection.vendor:
                self.stdout.write("Detected SQLite database")
                # SQLite doesn't support ALTER COLUMN directly
                # Django migrations should handle this, but let's check
                cursor.execute("PRAGMA table_info(users_user)")
                columns = cursor.fetchall()
                for col in columns:
                    if col[1] == 'role':
                        self.stdout.write(f"Current role field: {col}")
                        # Check max_length by trying to insert a long value
                        # Actually, we can't check max_length directly in SQLite
                        # We need to rely on Django migrations
                        break
                
                self.stdout.write(
                    self.style.WARNING(
                        "SQLite detected. Please run: python manage.py migrate users 0003"
                    )
                )
            else:
                # For PostgreSQL/MySQL, we can alter directly
                try:
                    cursor.execute(
                        "ALTER TABLE users_user ALTER COLUMN role TYPE VARCHAR(20)"
                    )
                    self.stdout.write(
                        self.style.SUCCESS("Successfully altered role field to VARCHAR(20)")
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error altering field: {e}")
                    )
        
        # Try to apply the migration
        from django.core.management import call_command
        self.stdout.write("Applying migration 0003...")
        call_command('migrate', 'users', '0003', verbosity=2)

