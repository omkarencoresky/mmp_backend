import uuid
from common_app.models import Permission, Role
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Assign default permissions to existing roles"

    def handle(self, *args, **kwargs):
        # Role names and their corresponding permissions
        role_permissions = {
            'travel_admin': "read,write,delete,update,all",
            'package_admin': "read,write,delete,update,all",
            'travel_sub_admin': "read,write",
            'package_sub_admin': "read,write",
        }

        for role_name, permissions in role_permissions.items():
            try:
                # Fetch the Role instance
                role = Role.objects.get(name=role_name)

                # Create Permission instance for the role
                Permission.objects.create(
                    role_id=role,  # Assign the Role instance
                    permission=permissions
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Permissions assigned to role '{role_name}' with permissions: {permissions}"
                    )
                )
            except Role.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Role '{role_name}' does not exist. Skipping.")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to assign permissions for role '{role_name}': {str(e)}")
                )