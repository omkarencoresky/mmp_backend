import uuid
from common_app.models import OAuthApplication
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Create OAuth application for the project"

    def handle(self, *args, **kwargs):
        OAuthApplication.objects.create(
            # name="mmp_app",
            client_id=str(uuid.uuid4()),
            client_secret=str(uuid.uuid4()),
            redirect_uri="http://localhost:8000/oauth/callback/",
            # client_type="confidential",
            # authorization_grant_type="authorization_code",
            # scope="read write",
            # is_active=True
        )
        self.stdout.write(self.style.SUCCESS("OAuth application created successfully"))
