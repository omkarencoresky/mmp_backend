import uuid

from utils.utils import *
from common_app.models import User
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from users.serializer.login_serializer import UserLoginSerializer
from users.serializer.register_serializer import UserRegistrationSerializer, UserUpdateSerializer


class Register(APIView):
    """
    A view that handles the registration of a new user.
    
    This view processes a POST request where user registration details are provided.
    It validates the data, checks for existing records (username, email, phone), 
    and optionally handles profile image uploads. If validation passes, it creates 
    a new user in the database.

    """
    
    def post(self, request: Request) -> Response:
        """
        Handles POST requests for user registration.

        This method:
        - Validates the provided user registration data using the `UserRegistrationSerializer`.
        - Checks for duplicate entries of username, email, or phone number.
        - Processes and optionally saves a profile image for the user.
        - Creates a new user record in the database upon successful validation.

        Args:
            request (Request): The HTTP request object containing user registration details, 
            including username, email, phone, role_id, and optional profile image.

        Returns:
            Response: A JSON response with a status code and message.
            - HTTP 201: User registered successfully.
            - HTTP 400: Validation errors.
            - HTTP 409: Duplicate username, email, or phone number.
            - HTTP 500: Unexpected error during registration.
        """

        try:
            serializer = UserRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                
                validated_data = serializer.validated_data
                profile_image = request.FILES.get('profile_url')

                format_validate = image_extension_validator(profile_image)

                if format_validate:
                    return format_validate

                return create_user(validated_data=validated_data, 
                        profile_image=profile_image
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
        
    

class Login(APIView):
    """
    A view that handles user login and authentication.

    This view processes a POST request containing the user's email and password.
    If the credentials are valid, an access token is generated and returned. 
    Otherwise, an error message is returned indicating the failure reason.

    """

    def post(self, request: Request, 
            user_id: uuid.UUID = None
        ) -> Response:
        """
        Handles POST requests for user login and authentication.

        This method:
        - Validates the provided login data using the `UserLoginSerializer`.
        - Verifies the existence of the provided phone number and country code.
        - Handles OTP-based login:
        - If `otp_input` is provided, verifies the OTP and authenticates the user.
        - If `otp_input` is not provided, generates and sends a new OTP to the user.
        - If authentication is successful, generates and returns an access token for the user.

        Args:
            request (Request): The HTTP request object containing login details such as phone_no, 
            country_code, and optional otp_input.

        Returns:
            Response: A JSON response with a status code and message.
            - HTTP 200: Successful login or OTP sent.
            - HTTP 400: Invalid or missing phone number.
            - HTTP 500: Unexpected error during login or OTP generation.
        """
        try:

            if user_id:

                user = get_user_by_id(user_id=user_id)
                
                if not user:
                    return create_response( 
                        success=False, 
                        message="User not found",
                        status=404
                    )
                
                form_data = request.POST
                otp_input = request.data.get('otp_input')

                if not otp_input:
                    return create_response(
                        success=False, 
                        message='OTP not provided.', 
                        status=400
                    )
                
                otp_verification, otp_message, status_code = verify_otp(user_id, otp_input)

                if not otp_verification:
                    return create_response(
                        success=False, 
                        message=otp_message, 
                        status=status_code
                    )
                
                access_token = generate_token(user)

                data = {
                    "user_id": user.id,
                    "token_type": access_token.token_type,
                    "access_token": access_token.access_token,
                    "expires_in": access_token.expires_at.strftime('%Y-%m-%d %H:%M:%S')
                }

                return create_response(
                    success=True, 
                    message="User login successfully.", 
                    data=data, 
                    status=200
                )


            serializer = UserLoginSerializer(data=request.data)

            if serializer.is_valid():   
                form_data = request.POST

                phone_no = form_data.get('phone_no')
                country_code = form_data.get('country_code')
                
                user = is_phone_number_exist(phone_no, country_code)

                if not user:
                    return create_response(
                        success=False,
                        message=f'Phone number not exist', 
                        status=404
                    )

                otp = generate_otp(user)

                if not otp:
                    return create_response(
                        success=False,
                        message=f'Some thing went wrong!', 
                        status=500
                    )

                send_otp_status = send_otp(country_code, phone_no, otp)

                if not send_otp_status:
                    return create_response(
                        success=False,
                        message=f'Something went wrong!', 
                        status=500
                    )

                return create_response(
                        success=True,
                        message=f'OTP send',
                        data={'user_id':user.id},
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
                message="Something went wrong!", 
                status=500
            )


class UserManagement(APIView):
    """
    A view that handles CRUD operations for User objects.

    This view allows retrieving, updating, and deleting user information. It supports fetching
    a single user or a list of users, and includes error handling for meaningful responses 
    in case of issues.

    Each method includes error handling to provide meaningful responses in case of issues.
    """
    def get(self, request: Request, 
            user_id: uuid.UUID=None
        ) -> Response:
        """
        Handles GET requests to retrieve user information.

        This method:
        - If `user_id` is provided, retrieves the details of the specified user.
        - If `user_id` is not provided, retrieves a list of all users.

        Args:
            request (Request): The HTTP request object.
            user_id (int, optional): The ID of the user to retrieve. Defaults to None.

        Returns:
            Response: A JSON response with a status code and message.
            - HTTP 200: User details or list of all users retrieved successfully.
            - HTTP 404: User with the specified ID not found.
            - HTTP 500: Unexpected error during retrieval.
        """

        try:
            if user_id:
                user = retrieve_user_details(user_id=user_id)
                
                if user is None:
                    return create_response( 
                        success=False, 
                        message="User not found",
                        data=[],
                        status=404
                    )
                
                return create_response( 
                        success=True, 
                        message="Retrieved successfully.", 
                        data=user,
                        status=200
                    )
                
            else:
                users = retrieve_user_details(user_id=None)
                
                return create_response( 
                        success=True, 
                        message="Retrieved users successfully.", 
                        data=users,
                        status=200,
                    )

        except Exception:
            return create_response( 
                success=False, 
                message="Something went wrong.", 
                status=500
            )
            
    def put(self, request: Request, 
            user_id: uuid.UUID
        ) -> Response:
        """
        Handles PUT requests to update user information.

        This method:
        - Checks if the user with the given `user_id` exists.
        - Validates the provided update data using the `UserRegistrationSerializer`.
        - Updates the user fields in the database if validation passes.

        Args:
            request (Request): The HTTP request object containing user update details.
            user_id (int): The ID of the user to update.

        Returns:
            Response: A JSON response with a status code and message.
            - HTTP 200: User updated successfully.
            - HTTP 400: Validation errors in the provided data.
            - HTTP 404: User with the specified ID not found.
            - HTTP 500: Unexpected error during update.
        """

        try:
            user = get_user_by_id(user_id=user_id)
            
            if user is None:
                return create_response(
                success=False,
                message="User Not found!",
                status=404
            )

            serializer =  UserUpdateSerializer(data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                user_update, message, status_code = update_record(user, validated_data)

                if not user_update:

                    return create_response(
                    success=False, 
                    message=message, 
                    status=status_code
                )

                profile_image = request.FILES.get('profile_url')

                if profile_image:
                    format_validate = image_extension_validator(profile_image)

                    if format_validate:
                        return format_validate

                    update_user_profile_image(user=user, profile_image=profile_image)

                user.save()
                return create_response(
                    success=True, 
                    message='Updated successfully.',
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

        except Exception as e:
            return create_response(
                success=False,
                message="Something went wrong!",
                status=500
            )


    def delete(self, request: Request, 
            user_id: uuid.UUID
        ) -> Response:
        """
        Handles DELETE requests to remove a user.

        This method:
        - Checks if the user with the given `user_id` exists.
        - Deletes the user record from the database if found.

        Args:
            request (Request): The HTTP request object.
            user_id (int): The ID of the user to delete.

        Returns:
            Response: A JSON response with a status code and message.
            - HTTP 200: User deleted successfully.
            - HTTP 404: User with the specified ID not found.
            - HTTP 500: Unexpected error during deletion.
        """

        try:
            user =  get_user_by_id(user_id=user_id)

            if user is None:
                return create_response(
                    success=False,
                    message="User not found",
                    status=404
                )
                
            user.delete()
            return create_response(
                success=True,
                message="Deleted successfully!",
                status=200
            )
                
        except Exception :
            return create_response(
                success=False,
                message="Something went wrong!",
                status=500
            )