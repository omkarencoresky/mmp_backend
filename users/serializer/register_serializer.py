from common_app.models import Role
from rest_framework import serializers
from utils.utils import create_response
from django.core.validators import RegexValidator

class UserRegistrationSerializer(serializers.Serializer):
    
    first_name = serializers.CharField(
        min_length=3, 
        max_length=100,
        validators=[RegexValidator(regex=r'^[a-zA-Z_]+$', 
                    message="first_name can only contain letters, numbers, and underscores.")],
        error_messages={
            'required': 'First name is required.',
            'max_length': 'First name must not exceed 100 characters.',
            'min_length': 'First name must be at least 3 characters long.',
        }
    )
    
    middle_name = serializers.CharField(
        required=False, 
        allow_blank=True, 
        max_length=100,
        validators=[RegexValidator(regex=r'^[a-zA-Z_]+$', 
                    message="middle_name can only contain letters, numbers, and underscores.")],
        error_messages={
            'max_length': 'Middle name must not exceed 100 characters.',
            'blank': 'Middle name cannot be blank if provided.',
        }
    )
    
    last_name = serializers.CharField(
        min_length=3, 
        max_length=100,
        validators=[RegexValidator(regex=r'^[a-zA-Z_]+$', 
                    message="last_name can only contain letters, numbers, and underscores.")],
        error_messages={
            'min_length': 'Last name must be at least 3 characters long.',
            'max_length': 'Last name must not exceed 100 characters.',
            'required': 'Last name is required.',
        }
    )
    
    email = serializers.EmailField(
        max_length=50,
        error_messages={
            'invalid': 'Enter a valid email address.',
            'max_length': 'Email must not exceed 50 characters.',
            'required': 'Email is required.',
            'blank': 'email field may not be blank',
        }
    )
    
    phone_no = serializers.CharField(
        min_length=10, 
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', 
                    message='''Phone number must be between 10 and 15 digits.''')],
        error_messages={
            'required': 'Phone number is required.',
            'blank': 'phone_no field may not be blank',
            'max_length': 'Phone number must not exceed 15 digits.',
            'min_length': 'Phone number must be at least 10 digits long.',
    }
    )
    
    gender = serializers.ChoiceField(
        choices=["male", "female", "other"],
        error_messages={
            'invalid_choice': 'Gender must be one of the following: male, female, or other.',
            'required': 'Gender is required.',
            'blank': 'gender field may not be blank',
        }
    )
    
    date_of_birth = serializers.DateField(
        required=False, 
        error_messages={
            'invalid': 'Enter a valid date for the date of birth.',
            'null': 'Date of birth cannot be null.',
            'blank': 'date_of_birth field may not be blank',
        }
    )
    
    password = serializers.CharField(
        min_length=8, 
        max_length=255, 
        write_only=True,
        validators=[RegexValidator(regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$', 
                                   message="Password must be at least 8 characters long and include both letters and numbers.")],
        error_messages={
            'min_length': 'Password must be at least 8 characters long.',
            'max_length': 'Password must not exceed 255 characters.',
            'required': 'Password is required.',
            'blank': 'password field may not be blank',
        }
    )
    
    role_id = serializers.UUIDField(
        error_messages={
            'required': 'Role is required.',
            'invalid': 'Role must be a valid UUID.',
            'blank': 'password field may not be blank',
        }
    )
    country_code = serializers.CharField(
        max_length=10, 
        error_messages={
            'required': 'Country code is required.',
            'max_length': 'Country code must not exceed 10 characters.',
            'blank': 'Country code field may not be blank',
        }
    )

    def validate_role_id(self, value):
        """
        Custom validation for role_id to check if the role exists.
        """
        try:
            role = Role.objects.get(id=value)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Role with this ID does not exist.")
        return value

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
