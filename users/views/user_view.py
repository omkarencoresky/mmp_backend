from utils.utils import *
from common_app.models import User
from rest_framework.views import APIView
from authentication.authentication import OAuthBackend
from users.serializer.login_serializer import UserLoginSerializer
from users.serializer.register_serializer import UserRegistrationSerializer

class Register(APIView):
    """
    A view that handles the registration of a new user.

    This view processes a POST request where user registration details are provided.
    It validates the data, checks for existing records (username, email, phone), 
    and optionally handles profile image uploads. If validation passes, it creates 
    a new user in the database.

    """
    
    def post(self, request):
        """
        Handles POST requests to register a new user.

        This method:
        - Validates the incoming registration data using the `UserRegistrationSerializer`.
        - Checks if the provided username, email, or phone number already exists in the database.
        - Optionally processes and saves a profile image.
        - Creates a new user if all validation checks pass.

        Args:
            request (Request): The HTTP request object containing user registration data, including username, 
            email, phone, and optional profile image.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 201: User registered successfully.
            - HTTP 400: Validation errors.
            - HTTP 409: Duplicate username, email, or phone.
            - HTTP 500: Unexpected error.
        """
        try:
            serializer = UserRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                
                validated_data = serializer.validated_data
                
                profile_image = request.FILES.get('profile_url')
                profile_url = None
               
                response = is_record_exists(
                    username=validated_data['username'], 
                    phone_no=validated_data['phone_no'],
                    email=validated_data['email']
                )
                
                if response:
                    return response

                if profile_image:
                    profile_url = save_image(profile_image,  validated_data.get('username'), 
                                    validated_data.get('role'))

                validated_data['profile_url'] = profile_url

                User.objects.create(**validated_data)
                return create_response(
                    success=True, 
                    message="User registered.", 
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



class Login(APIView):
    """
    A view that handles user login and authentication.

    This view processes a POST request containing the user's email and password.
    If the credentials are valid, an access token is generated and returned. 
    Otherwise, an error message is returned indicating the failure reason.

    """

    def post(self, request):
        """
        Handles POST requests to authenticate a user.

        This method:
        - Extracts the email and password from the request data.
        - Validates that both fields are provided.
        - Authenticates the user using the `OAuthBackend` authentication mechanism.
        - Generates an access token if authentication is successful.

        Args:
            request (Request): The HTTP request object containing user login credentials (email and password).

        Returns:
            Response: A JSON response with a status code and message.
            - On success (HTTP 200): success (bool), message (str), data (dict) with user ID, 
                access token, token type, and expiration.
            - On failure (HTTP 400/401): success (bool), message (str) with error details.
            - On error (HTTP 500): success (bool), message (str) with a generic error message.
        """
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():

                form_data = request.POST
                email = form_data.get('email')
                password = form_data.get('password')
                
                authenticate_user = OAuthBackend.authenticate(email=email, password=password)

                if authenticate_user is None:
                    return create_response(
                        success=False, 
                        message="Invalid email or password.", 
                        status=401
                    )
                    

                access_token = generate_token(authenticate_user)

                if access_token is None:
                    return create_response(
                        success=False, 
                        message="Something went wrong, Unable to generate token.", 
                        status=500
                    )

                data = {
                    "user_id": authenticate_user.id,
                    "access_token": access_token.access_token,
                    "token_type": access_token.token_type,
                    "expires_in": access_token.expires_at.strftime('%Y-%m-%d %H:%M:%S')
                }

                return create_response(
                    success=True, 
                    message="User logged In.", 
                    data=data, 
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

    This view provides methods to:
    - Retrieve a single user or a list of all users.
    - Update an existing user's information.
    - Delete a user.

    Each method includes error handling to provide meaningful responses in case of issues.
    """
    def get(self, request, user_id=None):
        """
        Handles GET requests to retrieve user information.

        This method:
        - If `user_id` is provided, retrieves the specific user with that ID.
        - If `user_id` is not provided, retrieves a list of all users.

        Args:
            request (Request): The HTTP request object.
            user_id (int, optional): The ID of the user to retrieve.

        Returns:
            Response: A JSON response with a status code and message.
            - On success (HTTP 200): success (bool), message (str), data (list).
            - On failure (HTTP 500): success (bool), message (str) with a generic error message.
        """
        try:
            if user_id:
                user = retrieve_user_details(id=user_id)

                if user is None:
                    return create_response( 
                        success=False, 
                        message="User not found",
                        status=404
                    )
                return create_response( 
                        success=True, 
                        message="User details", 
                        data=user,
                        status=200
                    )
                
            else:
                users = retrieve_user_details()
                
                # if users is None:
                #     return create_response( 
                #         success=False, 
                #         message="Users not found.", 
                #         status=400,
                #     )
                
                return create_response( 
                        success=True, 
                        message="Users list.", 
                        data=users,
                        status=200,
                    )

        except Exception as e:
            return create_response( 
                success=False, 
                message="Something went wrong.", 
                status=500
            )
            
    def put(self, request, user_id):
        """
        Handles PUT requests to update user information.

        This method:
        - Checks if the user with the given `user_id` exists.
        - Validates the request data against the UserRegistrationSerializer.
        - Updates the user fields if the validation passes.

        Args:
            request (Request): The HTTP request object containing user update data.
            user_id (int): The ID of the user to update.

        Returns:
            Response: A JSON response with a status code and message.
            - On success (HTTP 200): success (bool), message (str).
            - On validation failure (HTTP 400): success (bool), message (str) with validation errors.
            - On failure (HTTP 500): success (bool), message (str) with a generic error message.
        """
        try:
            user = get_user_by_id(user_id=user_id)
            
            if user is None:
                return create_response(
                success=False,
                message="User Not found!",
                status=404
            )
                
            serializer =  UserRegistrationSerializer(data=request.data, partial=True)
            
            if serializer.is_valid():
                form_data = serializer.validated_data
                
                for field, value in form_data.items():
                    setattr(user, field, value)
                    
                user.save()
                return create_response(
                    success=True, 
                    message='User updated!',
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
            
            
    def delete(self, request, user_id):
        """
        Handles DELETE requests to remove a user.

        This method:
        - Checks if the user with the given `user_id` exists.
        - Deletes the user if found.

        Args:
            request (Request): The HTTP request object.
            user_id (int): The ID of the user to delete.

        Returns:
            Response: A JSON response with a status code and message.
            - On success (HTTP 200): success (bool), message (str).
            - On failure (HTTP 404): success (bool), message (str) indicating user not found.
            - On error (HTTP 500): success (bool), message (str) with a generic error message.
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
                message="User deleted!",
                status=204
            )
                
        except Exception as e:
            return create_response(
                success=False,
                message="Something went wrong!",
                status=500
            )