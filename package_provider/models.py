import uuid
from django.db import models
from common_app.models import User

# Create your models here.
class TourPackage(models.Model):
    TRIP_TYPE_CHOICES = [
        ('honeymoon', 'Honeymoon'),
        ('adventure', 'Adventure'),
        ('winter', 'Winter'),
    ]

    PACKAGE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('inprogress', 'In Progress'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='package_provider_id')
    travel_agency_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_agency_id')
    package_name = models.CharField(max_length=255)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration_days = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    bidding_end_date = models.DateField()
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPE_CHOICES)
    deposit_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    cancellation_policy = models.BooleanField(default=True)
    itinerary_flexibility = models.BooleanField(default=True)
    included_services = models.TextField()
    excluded_services = models.TextField()
    package_status = models.CharField(max_length=20, choices=PACKAGE_STATUS_CHOICES, default='inactive')
    is_deleted = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tour_package'