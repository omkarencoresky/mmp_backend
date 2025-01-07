import uuid
from django.db import models
from common_app.models import User

# Create your models here.
class Driver(models.Model):
    LICENSE_TYPE_CHOICES = [
        ('two_wheeler', 'Two-Wheeler'),
        ('commercial', 'Commercial'),
        ('heavy_vehicle', 'Heavy Vehicle'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_user_id')
    experience_years = models.FloatField()
    hire_date = models.DateField(auto_now_add=True)
    license_number = models.CharField(max_length=50, unique=True)
    license_type = models.CharField(max_length=20, choices=LICENSE_TYPE_CHOICES, null=True)
    license_issue_date = models.DateField(null=True, blank=True)
    license_expiration_date = models.DateField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_no = models.CharField(max_length=15)
    is_deleted = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'driver'