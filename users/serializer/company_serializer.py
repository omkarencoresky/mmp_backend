import uuid

from rest_framework import serializers
from utils.utils import create_response
from common_app.models import User, Company
from django.core.validators import RegexValidator


class CompanySerializer(serializers.Serializer):
    COMPANY_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    company_name = serializers.CharField(
        max_length=255,
        required=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9\s\-&,]+$',
            message='Company name can only contain letters, numbers, spaces, hyphens, commas, and ampersands.'
        )],
        error_messages={
            'required': 'Company name is required.',
            'max_length': 'Company name cannot exceed 255 characters.',
        }
    )
    company_email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Company email is required.',
            'invalid': 'Invalid email format.',
        }
    )
    registration_number = serializers.CharField(
        max_length=50,
        required=True,
        validators=[RegexValidator(
            regex=r'^[A-Z0-9\-]+$',
            message='Registration number can only contain uppercase letters, numbers, and hyphens.'
        )],
        error_messages={
            'required': 'Registration number is required.',
            'max_length': 'Registration number cannot exceed 50 characters.',
        }
    )
    contact_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        validators=[RegexValidator(
            regex=r'^\+?[1-9]\d{1,14}$',
            message='Contact number must be a valid international phone number.'
        )],
        error_messages={
            'max_length': 'Contact number cannot exceed 20 characters.',
        }
    )
    foundation_date = serializers.DateField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'Invalid foundation date format.',
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
            'max_length': 'City name cannot exceed 100 characters.',
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
            'max_length': 'State name cannot exceed 100 characters.',
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
            'max_length': 'Country name cannot exceed 100 characters.',
        }
    )
    street_address = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9\s,.\-#]+$',
            message='Street address can only contain letters, numbers, spaces, commas, periods, hyphens, and hash symbols.'
        )],
        error_messages={
            'max_length': 'Street address cannot exceed 200 characters.',
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
            'max_length': 'Pin code cannot exceed 20 characters.',
        }
    )
    postal_code = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        validators=[RegexValidator(
            regex=r'^\d{5,10}$',
            message='Postal code must be between 5 and 10 digits.'
        )],
        error_messages={
            'max_length': 'Postal code cannot exceed 100 characters.',
        }
    )


    def validate_user_id(self, value):
        """
        Custom validation for user_id to check if the user exists.
        """
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return value
    

    def validate_registration_number(self, value):
        """
        Custom validation for user_id to check if the user exists.
        """
        company = Company.objects.filter(registration_number=value).exists()
        if company:
            raise serializers.ValidationError(f"Company already exist with '{value}'.")
        return value
    

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
