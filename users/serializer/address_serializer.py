from common_app.models import User
from rest_framework import serializers
from utils.utils import create_response
from django.core.validators import RegexValidator

class AddressSerializer(serializers.Serializer):
    
    city = serializers.CharField(
        max_length=100,
        min_length=2, 
        required=False, 
        allow_blank=True, 
        validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$', 
                    message='''City name can only contain letters and spaces.''')],
        error_messages={
            'max_length': 'City name must not exceed 100 characters.',
            'min_length': 'City must be at least 5 digits long.',
            'blank': 'City field may not be blank.',
        }
    )
    
    state = serializers.CharField(
        max_length=100, 
        min_length=2, 
        required=False, 
        allow_blank=True, 
        validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$', 
                    message='''State name can only contain letters and spaces.''')],
        error_messages={
            'max_length': 'State name must not exceed 100 characters.',
            'min_length': 'State must be at least 5 digits long.',
            'blank': 'State field may not be blank.',
        }
    )
    
    country = serializers.CharField(
        max_length=100, 
        min_length=2, 
        required=False, 
        allow_blank=True, 
        validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$', 
                    message='''Country name can only contain letters and spaces.''')],
        error_messages={
            'max_length': 'Country name must not exceed 100 characters.',
            'min_length': 'Country must be at least 5 digits long.',
            'blank': 'Country field may not be blank.',
        }
    )
    
    pin_code = serializers.CharField(
        max_length=20,
        required=False, 
        allow_blank=True, 
        validators=[RegexValidator(regex=r'^\d{5,10}$', 
                    message="Pin code must be between 5 and 10 digits.")],
        error_messages={
            'max_length': 'Pin code must not exceed 10 characters.',
            'min_length': 'Pin code must be at least 5 digits long.',
            'blank': 'Pin code field may not be blank.',
        }
    )
    
    street_address = serializers.CharField(
        max_length=200, 
        min_length=2, 
        required=False, 
        allow_blank=True, 
        validators=[RegexValidator(regex=r'^[\w\s,.-]+$', 
                    message='''Street address can only contain letters, numbers, spaces, commas, periods, and hyphens.''')],
        error_messages={
            'max_length': 'Street address must not exceed 200 characters.',
            'min_length': 'Street address must be at least 5 digits long.',
            'blank': 'Street address field may not be blank.',
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
