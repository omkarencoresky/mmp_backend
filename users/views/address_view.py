import uuid
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from common_app.models import User, User_Address
from users.serializer.address_serializer import AddressSerializer
from utils.utils import (create_response, is_user_id_exist, 
                         fetch_address_details, get_address_by_id, 
                         update_record)

class Addresses(APIView):
    """
    A view that handles CRUD operations for user address objects.

    The Addresses view handles CRUD operations for user addresses. It allows retrieving a
    specific address or a list of addresses associated with a user, adding new addresses, 
    updating existing ones, and deleting addresses. Each method performs necessary validation 
    and includes error handling to provide appropriate responses in case of issues, ensuring a 
    smooth user experience when managing address.

    """
    def get(self, request: Request,
            user_id: uuid.UUID=None,
            address_id: uuid.UUID=None,
        ) -> Response:
        """
        Handles GET requests to retrieve address information.

        This method can perform two types of operations:
        - Retrieve a specific address by its ID if `address_id` is provided.
        - List all addresses associated with a specific user if `user_id` is provided.

        Args:
            request (Request): The HTTP request object.
            address_id (uuid.UUID, optional): The ID of the address to retrieve.
            user_id (uuid.UUID, optional): The ID of the user whose addresses are to be listed.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 200: Address data successfully retrieved.
            - HTTP 404: Address not found (for `address_id` or `user_id`).
            - HTTP 500: Unexpected error.
        """
        try:
            if address_id:
                address = fetch_address_details(address_id=address_id)

                if not address:
                    return create_response( 
                        success=False,     
                        message='Addresses not found.',
                        status=404,
                    )
                
                return create_response(
                        success=True,     
                        message='Address Details.',
                        status=200,
                        data=address    
                    )                

            if user_id:
                addresses = fetch_address_details(user_id=user_id)
                
                if len(addresses) <= 0:
                    return create_response(
                        success=False,     
                        message='No address associate with this user.',
                        status=404
                    )

                return create_response(
                    success=True,     
                    message='User Addresses.',
                    status=200,
                    data=list(addresses)
                )
            
        except:
            return create_response(
                success=False, 
                message="Something went wrong!", 
                status=500
            )
        

    def post(self, request: Request, user_id: uuid.UUID) -> Response:
        """
        Handles POST requests to add a new address for a user.

        This method:
        - Validates the incoming address data using the `AddressSerializer`.
        - Checks if the address already exists for the user.
        - Creates a new address entry in the database if all validation checks pass.

        Args:
            request (Request): The HTTP request object containing address data (e.g., 
                city, state, pin_code).
            user_id (uuid.UUID): The ID of the user to associate the address with.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 201: Address successfully added.
            - HTTP 400: Validation errors.
            - HTTP 404: User not found.
            - HTTP 409: Address already exists for the user.
            - HTTP 500: Unexpected error.
        """
        try:
            if not is_user_id_exist(user_id=user_id):
                return create_response(
                    success=False,     
                    message='User not found.',
                    status=404,
                )

            serializer = AddressSerializer(data=request.data)

            if serializer.is_valid():
                form_data = serializer.validated_data
                
                if User_Address.objects.filter(user_id=user_id, **form_data).first():
                    return create_response(
                    success=False, 
                    message='Address already exist!',
                    status=403,
                )
                
                User_Address.objects.create(
                    user_id=User.objects.get(id=user_id),
                    **form_data
                )

                return create_response(
                    success=True, 
                    message='Address added!',
                    status=201,
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
        

    def delete(self, request: Request, address_id: uuid.UUID) -> Response:
        """
        Handles DELETE requests to remove a specific address.

        This method:
        - Deletes an address by its ID.

        Args:
            request (Request): The HTTP request object.
            address_id (uuid.UUID): The ID of the address to be deleted.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 204: Address successfully deleted.
            - HTTP 404: Address not found.
            - HTTP 500: Unexpected error.
        """
        try:
            address = get_address_by_id(address_id=address_id)
            
            if not address:
                return create_response(
                    success=False,
                    message="No address found.",
                    status=404
                )
            
            address.delete()
            return create_response(
                success=True,
                message="Address deleted!",
                status=200
            )
        
        except:
            return create_response(
                success=False, 
                message="Something went wrong!", 
                status=500
            )
        

    def put(self, request:Request, address_id: uuid.UUID) -> Response:
        """
        Handles PUT requests to update an existing address.

        This method:
        - Checks if the address with the provided address_id exists.
        - Validates the incoming data and updates the fields of the address.
        - Only updates the fields that are provided in the request using `partial=True`.

        Args:
            request (Request): The HTTP request object containing address data, which 
            can include any combination of the address fields to update.
            address_id (uuid.UUID): The ID of the address to be updated.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 200: Address successfully updated.
            - HTTP 400: Validation errors.
            - HTTP 404: Address not found.
            - HTTP 500: Internal server error.
        """
        try:
            address = get_address_by_id(address_id=address_id)
            
            if not address:
                return create_response(
                    success=False,
                    message="No address found.",
                    status=404
                )
            
            serializer = AddressSerializer(data=request.data, partial=True)

            if serializer.is_valid():

                form_data = serializer.validated_data

                address_update = update_record(address, form_data)

                if not address_update:
                    
                    return create_response(
                    success=False, 
                    message='Something went wrong', 
                    status=500
                )

                address.save()
                return create_response(
                    success=True, 
                    message='Address updated!',
                    status=200,
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