from rest_framework import serializers 
from django.core.validators import RegexValidator


class DailyItinerarySerializer(serializers.Serializer):
    # package_id = serializers.UUIDField(
    #     required=True,
    #     error_messages={
    #         'required': 'Package ID is required.',
    #     }
    # )

    itinerary_day = serializers.IntegerField(
        required=True,
        validators=[
            RegexValidator(
                r'^[0-9\s-]+$', 
                'Itinerary day must be a valid integer.'
            )
        ],
        error_messages={
            'required': 'Itinerary day is required.',
        }
    )
    activity_description = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Activity description is required.',
            'blank': 'Activity description cannot be blank.',
        }
    )
    pin_code = serializers.CharField(
        required=True,
        max_length=20,
        validators=[
            RegexValidator(
                r'^\d{5,10}$',  # Allows 5 to 10 digits only
                'Invalid pin code format. It must be between 5 to 10 numeric digits.'
            )
        ],
        error_messages={
            'required': 'Pin code is required.',
            'max_length': 'Pin code must not exceed 20 characters.',
        }
    )
    postal_code = serializers.CharField(
        required=False,
        max_length=50,
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9\s-]+$',  # Allows alphanumeric, spaces, and hyphens
                'Invalid postal code format. Only alphanumeric characters, spaces, and hyphens are allowed.'
            )
        ],
        error_messages={
            'max_length': 'Postal code must not exceed 50 characters.',
        }
    )
    city = serializers.CharField(
        required=True,
        max_length=100,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s]+$',  # Allows only letters and spaces
                'Invalid city name. Only letters and spaces are allowed.'
            )
        ],
        error_messages={
            'required': 'City is required.',
            'max_length': 'City must not exceed 100 characters.',
        }
    )
    state = serializers.CharField(
        required=True,
        max_length=100,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s]+$',  # Allows only letters and spaces
                'Invalid state name. Only letters and spaces are allowed.'
            )
        ],
        error_messages={
            'required': 'State is required.',
            'max_length': 'State must not exceed 100 characters.',
        }
    )
    country = serializers.CharField(
        required=True,
        max_length=100,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s]+$',  # Allows only letters and spaces
                'Invalid country name. Only letters and spaces are allowed.'
            )
        ],
        error_messages={
            'required': 'Country is required.',
            'max_length': 'Country must not exceed 100 characters.',
        }
    )
    street_address = serializers.CharField(
        required=True,
        max_length=200,
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9\s,.-]+$',  # Allows alphanumeric, spaces, commas, periods, and hyphens
                'Invalid street address. Only alphanumeric characters, spaces, commas, periods, and hyphens are allowed.'
            )
        ],
        error_messages={
            'required': 'Street address is required.',
            'max_length': 'Street address must not exceed 200 characters.',
        }
    )
    longitude = serializers.DecimalField(
        required=False,
        max_digits=9,
        decimal_places=6,
        error_messages={
            'invalid': 'Longitude must be a valid decimal.',
        }
    )
    latitude = serializers.DecimalField(
        required=False,
        max_digits=9,
        decimal_places=6,
        error_messages={
            'invalid': 'Latitude must be a valid decimal.',
        }
    )
    travel_mode = serializers.ChoiceField(
        choices=[
            ('car', 'Car'),
            ('bus', 'Bus'),
            ('train', 'Train'),
            ('flight', 'Flight'),
            ('boat', 'Boat'),
        ],
        required=True,
        error_messages={
            'required': 'Travel mode is required.',
            'invalid_choice': 'Travel mode must be one of car, bus, train, flight, or boat.',
        }
    )
    additional_info = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9\s,.-]*$',  # Optional but allows alphanumeric, spaces, commas, periods, and hyphens
                'Invalid additional info format. Only alphanumeric characters, spaces, commas, periods, and hyphens are allowed.'
            )
        ],
        error_messages={
            'blank': 'Additional info cannot be blank.',
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