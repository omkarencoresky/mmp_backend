import uuid
from django.core.management.base import BaseCommand
from common_app.models import Role

class Command(BaseCommand):
    help = "Add default roles to the roles table"

    def handle(self, *args, **kwargs):
        roles = [
            {'name': 'user', 'description': 'User role'},
            {'name': 'driver', 'description': 'Driver role'},
            {'name': 'travel_admin', 'description': 'Travel admin role'},
            {'name': 'package_admin', 'description': 'Package admin role'},
            {'name': 'travel_sub_admin', 'description': 'Travel sub-admin role'},
            {'name': 'package_sub_admin', 'description': 'Package sub-admin role'},
        ]

        for role in roles:
            obj, created = Role.objects.get_or_create(
                name=role['name'],
                defaults={
                    'id': uuid.uuid4(),
                    'description': role['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Role '{role['name']}' created successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"Role '{role['name']}' already exists"))

        self.stdout.write(self.style.SUCCESS("Default roles added successfully"))
