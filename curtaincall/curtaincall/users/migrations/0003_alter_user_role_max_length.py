# Generated manually to fix role field max_length

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('user', 'User'),
                    ('theater_manager', 'Theater Manager'),
                    ('superadmin', 'SuperAdmin')
                ],
                default='user',
                max_length=20
            ),
        ),
    ]
    
    # For SQLite, we need to handle the ALTER TABLE differently
    # Django will handle this automatically, but we ensure it's applied

