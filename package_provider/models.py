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
    travel_agency_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_agency_id', null=True, blank=True)
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


    
class DailyItinerary(models.Model):
    TRAVEL_MODE_CHOICES = [
        ('car', 'Car'),
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('flight', 'Flight'),
        ('boat', 'Boat'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    package_id = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='itinerary_package_id')
    itinerary_day = models.IntegerField(null=True, blank=True)
    activity_description = models.TextField(null=True, blank=True)
    pin_code = models.CharField(max_length=20, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    street_address = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    travel_mode = models.CharField( max_length=10, choices=TRAVEL_MODE_CHOICES, null=True, blank=True )
    additional_info = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'daily_itinerary'