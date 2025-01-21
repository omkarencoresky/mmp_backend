import uuid

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from common_app.models import Permission, Role
from common_app.serializer.permission_serializer import PermissionSerializer
from utils.utils import create_response, check_permissions, get_user_by_id, update_record


class PermissionManagement(APIView):
    """
    APIView for managing permissions.

    This class provides methods for CRUD operations on permissions,
    including retrieving, creating, updating, and deleting permissions
    for a specific user. The user permissions are validated before
    performing any operation.
    """

    def get(self, request: Request, 
            user_id: uuid.UUID, 
            permission_id: uuid.UUID=None,
        ) -> Response:

        """
        Retrieve permission details or a list of permissions for a user.

        Args:
            request (Request): The request object containing user and query parameters.
            user_id (uuid.UUID): The ID of the user whose permissions are being queried.
            permission_id (uuid.UUID, optional): The ID of the specific permission to retrieve. Defaults to None.

        Returns:
            Response: 
                - 200: Success with permission details or a list of permissions.
                - 404: User or permission not found.
                - 500: Internal server error.
        """

        try:

            user = get_user_by_id(user_id=user_id)

            if not user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )

            user_permission = check_permissions(user=user, permission_type='read')

            if user_permission:
                return user_permission

            if permission_id:
                permission = Permission.objects.filter(id=permission_id).values().first()
                
                if not permission:
                    return create_response(
                        success=False,
                        message='Permission not found.',
                        data=[],
                        status=404
                    )

                return create_response(
                        success=True,
                        message='Retrieved successfully.',
                        data=permission,
                        status=200
                    )

            else:

                permission_list = Permission.objects.filter(created_by=user_id).values().all()

                if not permission_list:
                    return create_response(
                        success=False,
                        message='Permission not found.',
                        data=[],
                        status=404
                    )

                return create_response(
                        success=True,
                        message='Retrieved Permissions successfully.',
                        data=list(permission_list),
                        status=200
                    )

        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )


    def post(self, request: Request, 
            user_id: uuid.UUID
        ) -> Response:

        """
        Create a new permission for a user.

        Args:
            request (Request): The request object containing permission data.
            user_id (uuid.UUID): The ID of the user creating the permission.

        Returns:
            Response: 
                - 201: Permission successfully created.
                - 400: Invalid input data.
                - 404: User not found or permission already exists.
                - 500: Internal server error.
        """

        try:
            user = get_user_by_id(user_id=user_id)

            if not user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )

            user_permission = check_permissions(user=user, permission_type='write')

            if user_permission:
                return user_permission

            serializer = PermissionSerializer(data=request.data)

            if serializer.is_valid():

                validated_data = serializer.validated_data
                validated_data['role_id'] = Role.objects.filter(id=validated_data['role_id']).first()
                validate_permission = Permission.objects.filter(role_id=validated_data['role_id']).first()

                if validate_permission:
                    return create_response(
                        success=False,
                        message='Permission already exist',
                        status=404
                    )

                Permission.objects.create(**validated_data)

                return create_response(
                    success=True,
                    message='Permission create.',
                    status=201
                )

            else:
                _, error_details = next(iter(serializer.errors.items()))
                error_message = error_details[0]

                return create_response(
                    success=False, 
                    message=error_message, 
                    status=400
                )

        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )

    def put(self, request: Request, 
            user_id: uuid.UUID, 
            permission_id: uuid.UUID=None,
        ) -> Response:

        """
        Update an existing permission for a user.

        Args:
            request (Request): The request object containing updated permission data.
            user_id (uuid.UUID): The ID of the user updating the permission.
            permission_id (uuid.UUID): The ID of the specific permission to update.

        Returns:
            Response: 
                - 201: Permission successfully updated.
                - 400: Invalid input data.
                - 404: User or permission not found.
                - 500: Internal server error.
        """

        try:

            user = get_user_by_id(user_id=user_id)
            permission = Permission.objects.filter(id=permission_id).first()

            if not user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )

            user_permission = check_permissions(user=user, permission_type='update')

            if user_permission:
                return user_permission

            serializer = PermissionSerializer(data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                if 'role_id' in validated_data.keys():
                    validated_data['role_id'] = Role.objects.filter(id=validated_data['role_id']).first()

                update_permission, message, status_code = update_record(permission, validated_data)
                
                if not update_permission:
                    return create_response(
                        success=False,
                        message=message,
                        status=status_code
                    )

                permission.save()
                return create_response(
                    success=True,
                    message='Permission update.',
                    status=200
                )

            else:
                _, error_details = next(iter(serializer.errors.items()))
                error_message = error_details[0]
                return create_response(
                    success=False, 
                    message=error_message, 
                    status=400
                )

        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )

    def delete(self, request: Request, 
            user_id: uuid.UUID, 
            permission_id: uuid.UUID=None,
        ) -> Response:

        """
        Delete a permission for a user.

        Args:
            request (Request): The request object.
            user_id (uuid.UUID): The ID of the user deleting the permission.
            permission_id (uuid.UUID): The ID of the specific permission to delete.

        Returns:
            Response: 
                - 204: Permission successfully deleted.
                - 404: User or permission not found.
                - 500: Internal server error.
        """

        try:

            user = get_user_by_id(user_id=user_id)
            permission = Permission.objects.filter(id=permission_id).first()

            if not user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )
            
            user_permission = check_permissions(user=user, permission_type='update')

            if user_permission:
                return user_permission
            
            permission.delete()
            return create_response(
                success=True,
                message='Permission delete',
                status=200
            )

        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )