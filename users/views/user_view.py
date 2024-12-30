from common_app.models import User
from rest_framework.views import APIView
from authentication.authentication import OAuthBackend
from users.serializer.login_serializer import UserLoginSerializer
from users.serializer.register_serializer import UserRegistrationSerializer
from utils.utils import save_image, is_record_exists, create_response, generate_token

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
                    message="User registered successfully", 
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
                    message="User logged in successfully.", 
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
                message="Something went wrong, try again later.", 
                status=500
            )


