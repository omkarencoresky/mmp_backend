import uuid

from common_app.models import User
from django.db import models

class TransportVehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('four_wheel', 'Four Wheel'),
        ('two_wheel', 'Two Wheel'),
    ]
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('gas', 'Gas'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_user_id')
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    owner_phone_no = models.CharField(max_length=15, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    seating_capacity = models.IntegerField()
    vehicle_identity_number = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, default='four_wheel')
    vehicle_category = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES, blank=True, null=True)
    registration_number = models.CharField(max_length=50, unique=True)
    insurance_policy_number = models.CharField(max_length=50, blank=True, null=True)
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    insurance_start_date = models.DateField(blank=True, null=True)
    insurance_end_date = models.DateField(blank=True, null=True)
    insurance_coverage_details = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transport_vehicle'