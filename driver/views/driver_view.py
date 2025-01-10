import uuid
from driver.models import Driver
from common_app.models import User
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from driver.serializer.driver_serializer import DriverSerializer
from utils.utils import create_response, get_user_by_id, update_record, validate_travel_agency_roles, check_permissions

class DriverManagement(APIView):
    """
    The DriverManagement class is an API view in Django REST Framework that manages 
    driver-related operations for a given user. It provides methods to handle the creation 
    (POST), retrieval (GET), update (PUT), and deletion (DELETE) of driver records. 
    The class uses DriverSerializer for data validation and utilities like create_response 
    and update_record for streamlined response handling and updates. It ensures data integrity 
    by validating user existence and preventing duplicate driver entries, offering clear error 
    handling for various scenarios such as missing data, validation failures, or server errors.
    
    """

    def get(self, request: Request, 
            user_id: uuid.UUID
        ) -> Response:
        """
        Handles GET requests to retrieve driver details.

        This method:
        - Fetches the driver's details using the `user_id`.
        - Returns the driver's details if found.

        Args:
            request (Request): The HTTP request object.
            user_id (uuid.UUID): The ID of the user to retrieve the driver details for.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 200: Driver details successfully retrieved.
            - HTTP 404: User not found.
            - HTTP 500: Internal server error.
        """

        try:
            user = Driver.objects.filter(user_id=user_id).values().first()

            if not user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                ) 
            
            return create_response(
                success= True, 
                message='User Details',
                data=user,
                status=200
            )

        except Exception as e:
            return create_response(
                success=False, 
                message='Something went wrong', 
                status=500
            )


    def post(self, request: Request, 
            user_id: uuid.UUID
        ) -> Response:
        
        """
        Handles POST requests to create a new driver.

        This method:
        - Validates the incoming data using `DriverSerializer`.
        - Checks if the user exists using the `user_id`.
        - Ensures no duplicate driver exists for the given user.
        - Creates a new driver record associated with the provided user.

        Args:
            request (Request): The HTTP request object containing driver data.
            user_id (uuid.UUID): The ID of the user to associate the driver with.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 201: Driver successfully created.
            - HTTP 400: Validation errors in the input data.
            - HTTP 404: User not found or driver already exists.
            - HTTP 500: Internal server error.
        """

        try:
            user = get_user_by_id(user_id=user_id)
            if not user:
                return create_response(
                    success=False,
                    message='User Not found',
                    status=404
                )
            
            serializer = DriverSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                if Driver.objects.filter(user_id=user_id).exists():

                    return create_response(
                        success=False,
                        message='Driver already exist.',
                        status=404
                    )
                
                Driver.objects.create(user_id=user, **validated_data)
                return create_response(
                    success=True,
                    message='Driver add successfully!',
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

        except Exception as e:
            return create_response(
                success=False, 
                message='Something went wrong', 
                status=500
            )
               

    def put(self, request: Request, 
            user_id: uuid.UUID,
            driver_id: uuid.UUID
        ) -> Response:
        """
        Handles PUT requests to update an existing driver.

        This method:
        - Fetches the driver record using the `user_id`.
        - Validates the incoming data using `DriverSerializer` (partial updates allowed).
        - Updates the driver record using `update_record` utility function.
        - Saves the changes to the database.

        Args:
            request (Request): The HTTP request object containing driver update data.
            user_id (uuid.UUID): The ID of the user whose driver details are to be updated.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 200: Driver details successfully updated.
            - HTTP 400: Validation errors in the input data.
            - HTTP 404: User not found.
            - HTTP 500: Internal server error.
        """

        try:
            user = get_user_by_id(user_id=user_id)
            
            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            validate_role = validate_travel_agency_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='write')
            
            if permission:
                return permission

            driver = Driver.objects.filter(id=driver_id).first()

            if not driver:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )

            serializer = DriverSerializer(data=request.data, partial=True) 

            if serializer.is_valid():
                validated_data = serializer.validated_data

                driver_instance = update_record(driver, validated_data)

                if not driver_instance:
                    
                    return create_response(
                    success=False, 
                    message='Something went wrong', 
                    status=500
                )

                driver.save()
                return create_response(
                    success= True, 
                    message='Driver Update',
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

        except Exception as e:
            return create_response(
                success=False, 
                message='Something went wrong', 
                status=500
            )
        
    def delete(self, request: Request, 
            user_id: uuid.UUID,
            driver_id: uuid.UUID
        ) -> Response:
        """
        Handles DELETE requests to delete a driver.

        This method:
        - Fetches the driver record using the `user_id`.
        - Deletes the driver record from the database if found.

        Args:
            request (Request): The HTTP request object.
            user_id (uuid.UUID): The ID of the user whose driver details are to be deleted.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 204: Driver successfully deleted.
            - HTTP 404: User not found.
            - HTTP 500: Internal server error.
        """
        
        try:
            user = get_user_by_id(user_id=user_id)
            
            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            validate_role = validate_travel_agency_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='delete')
            
            if permission:
                return permission

            driver = Driver.objects.filter(id=driver_id).first()

            if not driver:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                ) 
            
            driver.delete()
            return create_response(
                success= True, 
                message='Driver delete',
                status=204
            )

        except Exception as e:
            return create_response(
                success=False, 
                message='Something went wrong', 
                status=500
            )