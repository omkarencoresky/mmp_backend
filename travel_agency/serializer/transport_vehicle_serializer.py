from rest_framework import serializers
from utils.utils import create_response
from django.core.validators import RegexValidator

class TransportVehicleSerializer(serializers.Serializer):

    # user_id = serializers.UUIDField(
    #     error_messages={
    #         'required': 'User ID is required.',
    #         'invalid': 'User ID must be a valid UUID.',
    #     }
    # )

    owner_name = serializers.CharField(
        max_length=255,
        allow_blank=True,
        required=False,
        error_messages={
            'max_length': 'Owner name must not exceed 255 characters.',
            'blank': 'Owner name cannot be blank if provided.',
        }
    )

    owner_phone_no = serializers.CharField(
        min_length=10,
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', 
                    message='Phone number must be between 10 and 15 digits.')],
        error_messages={
            'required': 'Owner phone number is required.',
            'min_length': 'Phone number must be at least 10 digits.',
            'max_length': 'Phone number must not exceed 15 digits.',
            'blank': 'Phone number cannot be blank.',
        }
    )

    brand = serializers.CharField(
        max_length=50,
        error_messages={
            'required': 'Brand is required.',
            'max_length': 'Brand must not exceed 50 characters.',
        }
    )

    model = serializers.CharField(
        max_length=50,
        error_messages={
            'required': 'Model is required.',
            'max_length': 'Model must not exceed 50 characters.',
        }
    )

    seating_capacity = serializers.IntegerField(
        error_messages={
            'required': 'Seating capacity is required.',
            'invalid': 'Seating capacity must be a valid integer.',
        }
    )

    vehicle_identity_number = serializers.CharField(
        max_length=50,
        error_messages={
            'required': 'Vehicle identity number is required.',
            'max_length': 'Vehicle identity number must not exceed 50 characters.',
        }
    )

    vehicle_type = serializers.ChoiceField(
        choices=["four_wheel", "two_wheel"],
        error_messages={
            'invalid_choice': 'Vehicle type must be one of the following: four_wheel, two_wheel.',
            'required': 'Vehicle type is required.',
        }
    )

    vehicle_category = serializers.CharField(
        max_length=50,
        error_messages={
            'required': 'Vehicle category is required.',
            'max_length': 'Vehicle category must not exceed 50 characters.',
        }
    )

    fuel_type = serializers.ChoiceField(
        choices=["petrol", "diesel", "electric", "hybrid", "gas"],
        required=False,
        allow_blank=True,
        error_messages={
            'invalid_choice': 'Fuel type must be one of the following: petrol, diesel, electric, hybrid, gas.',
            'blank': 'Fuel type cannot be blank if provided.',
        }
    )

    registration_number = serializers.CharField(
        max_length=50,
        error_messages={
            'required': 'Registration number is required.',
            'max_length': 'Registration number must not exceed 50 characters.',
        }
    )

    insurance_policy_number = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'Insurance policy number must not exceed 50 characters.',
        }
    )

    insurance_provider = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'Insurance provider must not exceed 100 characters.',
        }
    )

    insurance_start_date = serializers.DateField(
        required=False,
        error_messages={
            'invalid': 'Insurance start date must be a valid date.',
        }
    )

    insurance_end_date = serializers.DateField(
        required=False,
        error_messages={
            'invalid': 'Insurance end date must be a valid date.',
        }
    )

    insurance_coverage_details = serializers.CharField(
        required=False,
        allow_blank=True,
        error_messages={
            'blank': 'Insurance coverage details cannot be blank if provided.',
        }
    )

    is_active = serializers.BooleanField(
        default=True,
        error_messages={
            'invalid': 'Is active must be a valid boolean.',
        }
    )

    is_deleted = serializers.BooleanField(
        default=False,
        error_messages={
            'invalid': 'Is deleted must be a valid boolean.',
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
