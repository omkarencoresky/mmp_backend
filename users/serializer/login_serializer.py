from rest_framework import serializers
from django.core.validators import RegexValidator

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    This serializer handles validation of user login data, including email and password.
    """
    email = serializers.EmailField(
        max_length=50,
        error_messages={
            'invalid': 'Enter a valid email address.',
            'max_length': 'Email must not exceed 50 characters.',
            'required': 'Email is required.',
            'blank': 'Email field may not be blank.',
        }
    )

    password = serializers.CharField(
        min_length=8,
        max_length=255,
        write_only=True,
        validators=[RegexValidator(regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$',
                    message='''Password must be at least 8 characters long and include both letters and numbers.''')],
        error_messages={
            'min_length': 'Password must be at least 8 characters long.',
            'max_length': 'Password must not exceed 255 characters.',
            'required': 'Password is required.',
            'blank': 'Password field may not be blank.',
        }
    )

    def validate(self, data):
        """
        Custom validation for the login data.

        Ensures that both email and password are provided and follow the expected formats.
        """
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError({'email': 'Email is required.'})
        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'})

        return data
