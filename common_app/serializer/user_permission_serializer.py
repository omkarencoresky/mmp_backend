from common_app.models import User
from rest_framework import serializers
from utils.utils import create_response
from django.core.validators import RegexValidator


class UserPermissionSerializer(serializers.Serializer):

    user_id = serializers.UUIDField(
        error_messages={
            'required': 'User ID is required.',
            'blank': 'User ID may not be blank.',
            'invalid': 'User ID must be a valid UUID.'
        }
    )


    permission = serializers.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z, ]+$',
                message='Permission must contain only letters (uppercase or lowercase), commas, and spaces.'
            )
        ],
        error_messages={
            'required': 'Permission is required.',
            'max_length': 'Permission must not exceed 100 characters.',
            'blank': 'Permission may not be blank.',
        }
    )

    is_active = serializers.BooleanField(
        required=False,
        error_messages={
            'required': 'is_active field is required.',
            'invalid': 'Is_active allow only true or false.'
        }
    )

    def validate_user_id(self, value):
        """
        Validate the user_id field to ensure it exists in the database.
        """
        validated_user = User.objects.filter(id=value).first()
        if not validated_user:
            raise serializers.ValidationError('Invalid user ID.')
        return value


    def validate_permission(self, value):
        """
        Validate the permission field to ensure it's in the correct format and exists in the permission_choices.
        """
        valid_permissions = ['read', 'write', 'delete', 'update']
        permissions_list = value.split(',')
        
        invalid_permissions = [
            perm.strip() for perm in permissions_list if perm.strip() not in valid_permissions
        ]
        
        if invalid_permissions:
            raise serializers.ValidationError(f"Invalid permissions: {', '.join(invalid_permissions)}")
        
        return ','.join([perm.strip() for perm in permissions_list])


    def validate(self, data):
        """
        General validation method.
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
                create_response(success=False, message=errors, status=404)
            )
        
        return data
