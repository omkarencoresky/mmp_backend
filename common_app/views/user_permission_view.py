import uuid

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from common_app.models import UserPermission
from common_app.serializer.user_permission_serializer import UserPermissionSerializer
from utils.utils import create_response, get_user_by_id, validate_roles_for_company, check_permissions


class UserPermissionManagement(APIView):

    def get(self, request: Request, 
            granted_by: uuid.UUID,
            user_id: uuid.UUID=None,
        ) -> Response:

        try:
            grant_user = get_user_by_id(user_id=granted_by)

            if not grant_user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )
            
            user_permission = check_permissions(user=grant_user, permission_type='write')

            if user_permission:
                return user_permission
            
            if user_id:
                user_permission = UserPermission.objects.filter(user_id=user_id).first()

                if not user_permission:
                    return create_response(
                        success=False,
                        message='User Permission not found.',
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='User permission detail.',
                    data=user_permission,
                    status=200
                )
            
            else:
                permission_list = UserPermission.objects.filter(granted_by=granted_by).values().all()

                if not permission_list:
                    return create_response(
                        success=False,
                        message='User Permission not found.',
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='User permission detail.',
                    data=list(permission_list),
                    status=200
                )

        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )


    def post(self, request: Request, granted_by: uuid.UUID) -> Response:
        try:
            grant_user = get_user_by_id(user_id=granted_by)

            if not grant_user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )
            
            user_permission = check_permissions(user=grant_user, permission_type='write')

            if user_permission:
                return user_permission

            serializer = UserPermissionSerializer(data=request.data)    

            if serializer.is_valid():
                validated_data = serializer.validated_data
                user = get_user_by_id(user_id=validated_data['user_id'])

                if not user:
                    return create_response(
                        success=False,
                        message='User not found.',
                        status=404
                    )

                validate_permission = UserPermission.objects.filter(user_id=user).first()

                if validate_permission:
                    return create_response(
                        success=False,
                        message='User Permission already exist.',
                        status=404
                    )

                UserPermission.objects.create(user_id=user, 
                                    granted_by=grant_user, 
                                    permission=validated_data['permission']
                                )

                return create_response(
                    success=True,
                    message='Permission created.',
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


    def put(self, request: Request) -> Response:
        try:
            pass

        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )


    def delete(self, request: Request) -> Response:
        try:
            pass

        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )