import uuid
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from package_provider.models import TourPackage
from common_app.models import User, Permission, Role
from package_provider.serializer.tour_serializer import TourPackageSerializer
from utils.utils import create_response, get_user_by_id, update_record, check_permissions, validate_package_provider_roles

class TourPackageManagement(APIView):
    """
    API View for managing tour packages.

    This view provides endpoints for performing CRUD operations on tour packages.
    Each method checks user permissions based on their role and permissions 
    before proceeding with the requested operation.

    """

    def get(self, request: Request, 
            user_id: uuid.UUID,
            package_id: uuid.UUID=None, 
        ) -> Response:

        """
        Retrieve tour package details or a list of packages for a user.

        Args:
            request (Request): The request object containing user and query parameters.
            user_id (uuid.UUID): The ID of the user whose packages are being queried.
            package_id (uuid.UUID): The ID of the specific package to retrieve.

        Returns:
            Response: 
                - 200: Success with package details or list of packages.
                - 404: Package not found or no packages associated with the user.
                - 500: Internal server error.
        """

        try:
            user = get_user_by_id(user_id=user_id)
            validate_role = validate_package_provider_roles(user=user)

            if validate_role:
                return validate_role

            permission = check_permissions(user=user, permission_type='read')
            
            if permission:
                return permission     

            if package_id:
                package = TourPackage.objects.filter(id=package_id).values().first()

                if not package:
                    return create_response(
                        success=False,
                        message='Package not found.',
                        data=[],
                        status=404
                    )
                
                
                return create_response (
                    success=True,
                    message='Retrieved successfully.',
                    data=package,
                    status=200
                )

            else:
                user_packages = TourPackage.objects.filter(user_id=user_id).values().all() 

                if not user_packages:
                    return create_response(
                        success=False,
                        message='No package associated with this user.',
                        data=[],
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='Retrieved packages successfully.',
                    data=list(user_packages),
                    status=200
                )

        except:
            return create_response(
                success=False,
                message="Something went wrong!",
                status=500
            )
        

    def post(
            self, request: Request, 
            user_id: uuid.UUID
        ) -> Response:

        """
        Create a new tour package for a user.

        Args:
            request (Request): The request object containing the package data.
            user_id (uuid.UUID): The ID of the user creating the package.

        Returns:
            Response: 
                - 201: Tour package created successfully.
                - 404: User not found or permission denied.
                - 400: Validation error for the provided data.
                - 500: Internal server error.
        """
        
        try:
            user = get_user_by_id(user_id=user_id)
            
            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            validate_role = validate_package_provider_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='write')
            
            if permission:
                return permission
            
            serializer = TourPackageSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                tour_package_instance = TourPackage.objects.filter(user_id=user_id, **validated_data)

                if tour_package_instance:
                    return create_response(
                        success=False,
                        message='This package already exist',
                        status=404
                    )
                
                TourPackage.objects.create(user_id=user, **validated_data)

                return create_response(
                    success=True,
                    message='Tour package created.',
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
                message="Something went wrong!",
                status=500
            )
               
    
    def put(self, request: Request, 
            user_id: uuid.UUID=None,
            package_id: uuid.UUID=None
        ) -> Response:

        """
        Update an existing tour package.

        Args:
            request (Request): The request object containing the updated data.
            user_id (uuid.UUID): The ID of the user associated with the package.
            package_id (uuid.UUID): The ID of the package to update.

        Returns:
            Response: 
                - 200: Package updated successfully.
                - 404: Package not found or permission denied.
                - 400: Validation error for the provided data.
                - 500: Internal server error.
        """

        try:
            package = TourPackage.objects.filter(id=package_id, user_id=user_id).first()
            user = get_user_by_id(user_id=user_id)
            
            if not package:
                return create_response(
                    success=False,
                    message='Package not found.',
                    status=404
                )
            
            validate_role = validate_package_provider_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='update')

            if permission:
                return permission
            
            serializer = TourPackageSerializer(data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                package_update, message, status_code = update_record(package, validated_data)

                if not package_update:
                    return create_response(
                        success=False,
                        message=message,
                        status=status_code
                    )
                
                package.save()
                return create_response(
                    success=True,
                    message='Tour package updated.',
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
            user_id: uuid.UUID=None,
            package_id: uuid.UUID=None
        ) -> Response:

        """
        Delete a specific tour package.

        Args:
            request (Request): The request object containing user and package IDs.
            user_id (uuid.UUID): The ID of the user associated with the package.
            package_id (uuid.UUID): The ID of the package to delete.

        Returns:
            Response: 
                - 204: Package deleted successfully.
                - 404: Package not found or permission denied.
                - 500: Internal server error.
        """

        try:
            package = TourPackage.objects.filter(id=package_id, user_id=user_id).first()
            user = get_user_by_id(user_id=user_id)

            if not package:
                return create_response(
                    success=False,
                    message='Tour package not found',
                    status=404
                )
            
            validate_role = validate_package_provider_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='delete')

            if permission:
                return permission
            
            package.delete()
            return create_response(
                success=True,
                message='Tour package delete.',
                status=200
            )
        
        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )