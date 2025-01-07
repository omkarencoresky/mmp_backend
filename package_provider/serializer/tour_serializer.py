from rest_framework import serializers
from django.core.validators import RegexValidator

class TourPackageSerializer(serializers.Serializer):
    package_name = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={
            'required': 'Package name is required.',
            'max_length': 'Package name must not exceed 255 characters.',
            'blank': 'package name field may not be blank',
        }
    )
    description = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Description is required.',
        }
    )
    base_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        error_messages={
            'invalid': 'Base price must be a valid decimal.',
            'required': 'Base price is required.',
            'blank': 'Base price field may not be blank',
        }
    )
    discount_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        required=False,
        error_messages={
            'invalid': 'Discount price must be a valid decimal.',
            'blank': 'Discount price field may not be blank',
        }
    )
    duration_days = serializers.IntegerField(
        required=True,
        error_messages={
            'invalid': 'Duration days must be a valid integer.',
            'required': 'Duration days are required.',
            'blank': 'Duration days field may not be blank',
        }
    )
    start_date = serializers.DateField(
        required=True,
        error_messages={
            'invalid': 'Start date must be a valid date.',
            'required': 'Start date is required.',
            'blank': 'Start date field may not be blank',
        }
    )
    end_date = serializers.DateField(
        required=True,
        error_messages={
            'invalid': 'End date must be a valid date.',
            'required': 'End date is required.',
            'blank': 'End date field may not be blank',
        }
    )
    bidding_end_date = serializers.DateField(
        required=True,
        error_messages={
            'invalid': 'Bidding end date must be a valid date.',
            'required': 'Bidding end date is required.',
            'blank': 'Bidding end date field may not be blank',
        }
    )
    trip_type = serializers.ChoiceField(
        choices=[
            ('honeymoon', 'Honeymoon'),
            ('adventure', 'Adventure'),
            ('winter', 'Winter'),
        ],
        required=True,
        error_messages={
            'required': 'Trip type is required.',
            'invalid_choice': 'Trip type must be one of this honeymoon, adventure, or winter.',
            'blank': 'Trip type field may not be blank',
        }
    )
    deposit_percentage = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        error_messages={
            'invalid': 'Deposit percentage must be a valid decimal.',
            'required': 'Deposit percentage is required.',
        }
    )
    cancellation_policy = serializers.BooleanField(
        required=False,
        default=True,
        error_messages={
            'invalid': 'Cancellation policy must be a valid boolean.',
        }
    )
    itinerary_flexibility = serializers.BooleanField(
        required=False,
        default=True,
        error_messages={
            'invalid': 'Itinerary flexibility must be a valid boolean.',
        }
    )
    included_services = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Included services are required.',
        }
    )
    excluded_services = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Excluded services are required.',
        }
    )
    package_status = serializers.ChoiceField(
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('inprogress', 'In Progress'),
        ],
        default='inactive',
        required=False,
        error_messages={
            'invalid_choice': 'Package status must be one of this active, inactive, or in progress.',
        }
    )

    def validate(self, data):
        """
        Custom validation for the fields, ensuring all required validations pass.
        """
        errors = {}
        for field, value in data.items():
            field_instance = self.fields.get(field)
            try:
                field_instance.run_validation(value)
            except serializers.ValidationError as e:
                errors[field] = e.detail

        if errors:
            raise serializers.ValidationError(errors)
        return data
