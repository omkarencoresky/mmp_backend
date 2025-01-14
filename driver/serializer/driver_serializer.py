from rest_framework import serializers
from utils.utils import create_response
from django.core.validators import RegexValidator


class DriverSerializer(serializers.Serializer):
    LICENSE_TYPE_CHOICES = [
        ('two_wheeler', 'Two-Wheeler'),
        ('commercial', 'Commercial'),
        ('heavy_vehicle', 'Heavy Vehicle'),
    ]
    

    experience_years = serializers.FloatField(
        min_value=0,
        error_messages={
            'required': 'Experience years is required.',
            'invalid': 'Experience years must be a valid number.',
            'min_value': 'Experience years cannot be negative.',
        }
    )
    
    license_number = serializers.CharField(
        max_length=50,
        validators=[RegexValidator(regex=r'^[A-Z0-9]+$', 
                    message='License number must contain only uppercase letters and numbers.')],
        error_messages={
            'required': 'License number is required.',
            'unique': 'License number must be unique.',
            'max_length': 'License number must not exceed 50 characters.',
            'blank': 'License number may not be blank.',
        }
    )
    
    license_type = serializers.ChoiceField(
        choices=LICENSE_TYPE_CHOICES,
        required=False,
        allow_null=True,
        error_messages={
            'invalid_choice': 'License type must be one of the following: two-wheeler, commercial, heavy Vehicle.',
            'blank': 'License issue date may not be blank.',
            'null': 'License type may not be null.',
        }
    )
    
    license_issue_date = serializers.DateField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'Enter a valid date for the license issue date.',
            'null': 'License issue date may not be null.',
            'blank': 'License issue date may not be blank.',
        }
    )
    
    license_expiration_date = serializers.DateField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'Enter a valid date for the license expiration date.',
            'null': 'License expiration date may not be null.',
            'blank': 'License expiration date may not be blank.',
        }
    )
    
    emergency_contact_name = serializers.CharField(
        max_length=255,
        validators=[RegexValidator(regex=r'^[a-zA-Z ]+$', 
                    message='Emergency contact name must contain only letters and spaces.')],
        error_messages={
            'required': 'Emergency contact name is required.',
            'max_length': 'Emergency contact name must not exceed 255 characters.',
            'blank': 'Emergency contact name may not be blank.',
        }
    )
    
    emergency_contact_no = serializers.CharField(
        min_length=10, 
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', 
                    message='Emergency contact number must be between 10 and 15 digits.')],
        error_messages={
            'required': 'Emergency contact number is required.',
            'blank': 'Emergency contact number may not be blank.',
            'max_length': 'Emergency contact number must not exceed 15 digits.',
            'min_length': 'Emergency contact number must be at least 10 digits long.',
        }
    )

    def validate(self, data):
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
