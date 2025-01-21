from common_app.models import Role
from rest_framework import serializers
from utils.utils import create_response
from django.core.validators import RegexValidator


class PermissionSerializer(serializers.Serializer):    

    # role_id = serializers.UUIDField(
    #     error_messages={
    #         'required': 'Role ID is required.',
    #         'blank': 'Role ID may not be blank.',
    #         'invalid': 'Role ID must be a valid UUID.'
    #     }
    # )
    
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

    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        error_messages={
            'max_length': 'Description must not exceed 500 characters.',
        }
    )

    # def validate_role_id(self, value):
    #     """
    #     Validate the role_id field to ensure it exists in the database.
    #     """
    #     validated_role = Role.objects.filter(id=value).first()
    #     if not validated_role:
    #         raise serializers.ValidationError('Invalid role ID.')
    #     return value


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
