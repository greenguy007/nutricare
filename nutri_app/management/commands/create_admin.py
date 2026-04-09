"""
Management command to create default admin user if it doesn't exist.
Called on every startup so Render always has an admin account.
"""
from django.core.management.base import BaseCommand
from ...models import Login


class Command(BaseCommand):
    help = 'Create default admin user if it does not exist'

    def handle(self, *args, **options):
        if not Login.objects.filter(username='admin').exists():
            admin = Login.objects.create_superuser(
                username='admin',
                email='admin@nutricare.com',
                password='Admin@123',
                usertype='admin',
                is_active=True,
                is_verified=True,
                viewpassword='Admin@123',
            )
            self.stdout.write(self.style.SUCCESS('Default admin created: admin / Admin@123'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin already exists, skipping.'))
