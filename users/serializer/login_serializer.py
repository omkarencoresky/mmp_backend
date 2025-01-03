from rest_framework import serializers
from django.core.validators import RegexValidator

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login using phone number and OTP.

    This serializer handles validation of login data, including phone number, 
    country code, and optionally OTP input for authentication.
    """

    phone_no = serializers.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\d{10,15}$',
                                   message='Phone number must be between 10 and 15 digits.')],
        error_messages={
            'max_length': 'Phone number must not exceed 15 digits.',
            'required': 'Phone number is required.',
            'blank': 'Phone number field may not be blank.',
        }
    )

    country_code = serializers.CharField(
        max_length=5,
        validators=[RegexValidator(regex=r'^\+\d{1,4}$',
                                   message='Country code must start with "+" followed by 1-4 digits.')],
        error_messages={
            'max_length': 'Country code must not exceed 5 characters.',
            'required': 'Country code is required.',
            'blank': 'Country code field may not be blank.',
        }
    )

    otp_input = serializers.CharField(
        max_length=6,
        required=False,
        validators=[RegexValidator(regex=r'^\d{6}$',
                                   message='OTP must be a 6-digit number.')],
        error_messages={
            'max_length': 'OTP must not exceed 6 digits.',
            'blank': 'OTP field may not be blank if provided.',
        }
    )

    def validate(self, data):
        """
        Custom validation for the login data.

        Ensures that both phone_no and country_code are provided,
        and optionally validates OTP if it's part of the input.
        """
        phone_no = data.get('phone_no')
        country_code = data.get('country_code')
        otp_input = data.get('otp_input')

        if not phone_no:
            raise serializers.ValidationError({'phone_no': 'Phone number is required.'})
        if not country_code:
            raise serializers.ValidationError({'country_code': 'Country code is required.'})

        if otp_input and len(otp_input) != 6:
            raise serializers.ValidationError({'otp_input': 'OTP must be exactly 6 digits.'})

        return data
