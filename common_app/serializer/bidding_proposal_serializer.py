from rest_framework import serializers
from utils.utils import create_response
from django.core.validators import MinValueValidator


class TourPackageBidSerializer(serializers.Serializer):
    
    package_necessities_id = serializers.UUIDField(
        error_messages={
            'required': 'Package necessities ID is required.',
            'blank': 'Package necessities ID may not be blank.',
            'invalid': 'Package necessities ID must be a valid UUID.',
        }
    )
    travel_agency_id = serializers.UUIDField(
        error_messages={
            'required': 'Travel agency ID is required.',
            'blank': 'Travel agency ID may not be blank.',
            'invalid': 'Travel agency ID must be a valid UUID.',
        }
    )
    bid_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        error_messages={
            'required': 'Bid price is required.',
            'blank': 'Bid price may not be blank.',
            'invalid': 'Bid price must be a valid decimal.',
            'max_digits': 'Bid price must not exceed 10 digits in total.',
            'max_decimal_places': 'Bid price must not have more than 2 decimal places.',
        }
    )
    bid_status = serializers.ChoiceField(
        choices=[('pending', 'pending'), ('bidded', 'bidded'), ('accepted', 'accepted'), ('rejected', 'rejected')],
        default='pending',
        error_messages={
            'invalid_choice': 'Invalid choice for bid status.',
        }
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        error_messages={
            'max_length': 'Description must not exceed 500 characters.',
        }
    )


    def validate(self, data):
        """
        General validation method for additional rules.
        """
        errors = {}
        for field, value in data.items():
            field_instance = self.fields.get(field)
            try:
                if field_instance:
                    field_instance.run_validation(value)
            except serializers.ValidationError as e:
                if isinstance(e.detail, list):
                    errors[field] = e.detail[0]
                else:
                    errors[field] = e.detail

        if errors:
            raise serializers.ValidationError(
                create_response(success=False, message=errors, status=400)
            )
        return data
