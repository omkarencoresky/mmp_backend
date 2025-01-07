from common_app.models import User
from rest_framework import serializers
from utils.utils import create_response
from django.core.validators import RegexValidator

class AddressSerializer(serializers.Serializer):
    
    house_no = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'House number must not exceed 20 characters.',
        }
    )
    apartment = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'Apartment name must not exceed 50 characters.',
        }
    )
    nearest_landmark = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'Landmark must not exceed 100 characters.',
        }
    )
    city = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z\s]+$',
            message='City name can only contain letters and spaces.'
        )],
        error_messages={
            'max_length': 'City name must not exceed 100 characters.',
        }
    )
    state = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z\s]+$',
            message='State name can only contain letters and spaces.'
        )],
        error_messages={
            'max_length': 'State name must not exceed 100 characters.',
        }
    )
    country = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z\s]+$',
            message='Country name can only contain letters and spaces.'
        )],
        error_messages={
            'max_length': 'Country name must not exceed 100 characters.',
        }
    )
    street_address = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        validators=[RegexValidator(
            regex=r'^[\w\s,.-]+$',
            message='Street address only contain letters, numbers, spaces, commas, periods, and hyphens.'
        )],
        error_messages={
            'max_length': 'Street address must not exceed 200 characters.',
        }
    )
    pin_code = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        validators=[RegexValidator(
            regex=r'^\d{5,10}$',
            message='Pin code must be between 5 and 10 digits.'
        )],
        error_messages={
            'max_length': 'Pin code must not exceed 20 characters.',
        }
    )
    postal_code = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'Postal code must not exceed 100 characters.',
        }
    )
    latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'Invalid latitude format.',
        }
    )
    longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'Invalid longitude format.',
        }
    )


    def validate(self, data):
        """
        Custom validation for the fields, returns errors if any field validation fails.
        """
        errors = {}

        for field, value in data.items():
            field_instance = self.fields.get(field)

            try:
                field_instance.run_validation(value)
            except serializers.ValidationError as e:
                error_message = list(e.detail.values())[0][0]
                errors[field] = error_message

            if errors:
                return create_response(success=False, message=errors, status=404)
        
        return data
