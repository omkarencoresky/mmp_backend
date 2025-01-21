from rest_framework import serializers
from django.core.validators import RegexValidator

class TourPackageNecessitySerializer(serializers.Serializer):
    vehicle_type_id = serializers.UUIDField(
        required=True,
        error_messages={
            'required': 'Vehicle type ID is required.',
            'invalid': 'Vehicle type ID must be a valid UUID.',
        }
    )
    tour_package_id = serializers.UUIDField(
        required=True,
        error_messages={
            'required': 'Tour package ID is required.',
            'invalid': 'Tour package ID must be a valid UUID.',
        }
    )
    approved_proposal_id = serializers.UUIDField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'Approved proposal ID must be a valid UUID.',
        }
    )
    vehicle_name = serializers.CharField(
        max_length=100,
        required=True,
        error_messages={
            'required': 'Vehicle name is required.',
            'max_length': 'Vehicle name must not exceed 100 characters.',
            'blank': 'Vehicle name field may not be blank.',
        }
    )
    decided_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        error_messages={
            'required': 'Decided price is required.',
            'invalid': 'Decided price must be a valid decimal.',
        }
    )
    seating_capacity = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'Seating capacity is required.',
            'invalid': 'Seating capacity must be a valid integer.',
            'blank': 'Seating capacity field may not be blank.',
        }
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        error_messages={
            'invalid': 'Description must be a valid string.',
        }
    )
    # bid_status = serializers.ChoiceField(
    #     choices=['pending', 'bidded', 'accepted', 'rejected'],
    #     required=False,
    #     default='pending',
    #     error_messages={
    #         'invalid_choice': 'Invalid choice for bid status.',
    #     }
    # )
    def validate(self, data):
        """
        Custom validation for the serializer to ensure all validations pass.
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





class TourPackageAcceptSerializer(serializers.Serializer):
    approved_proposal_id = serializers.UUIDField(
        required=True,
        error_messages={
            'required': 'Vehicle type ID is required.',
            'invalid': 'Vehicle type ID must be a valid UUID.',
        }
    )
    
    def validate(self, data):
        """
        Custom validation for the serializer to ensure all validations pass.
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
