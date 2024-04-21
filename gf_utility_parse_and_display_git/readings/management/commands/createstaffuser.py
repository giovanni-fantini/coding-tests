from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a staff user authorised to view, change and search readings in the admin site'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        staff_users_query_set = User.objects.filter(is_staff=True)
        if staff_users_query_set:
            self.stdout.write(f'Staff user already exists, username: {staff_users_query_set.first()}')
        else:
            u = User.objects.create_user('admin', password='admin')
            u.is_superuser = False
            u.is_staff = True
            u.save()
            self.stdout.write(f'Staff user created with username: admin, password: admin')