from django.views import View
from rest_framework import status
from common_app.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from utils.utils import save_image, is_record_exists, custom_response
from users.serializer.register_serializer import UserRegistrationSerializer
# from users. import validate_user_register, validate_user_login
# from .validators import email_exist, username_exist, phone_number_exist

class Register(APIView):
    """
    A view that handles user registration.

    This view processes a POST request to register a new user. It validates the provided data,
    checks for duplicate records (username, email, and phone number), and handles optional 
    profile image uploads. If validation passes, a new user is created and stored in the database.

    Attributes:
        None

    Methods:
        post(request, *args, **kwargs):
            Handles the user registration process, including validation, duplicate checks,
            profile image handling, and user creation.

    Responses:
        - HTTP 201 (Created): On successful user registration.
        - HTTP 400 (Bad Request): If validation errors occur.
        - HTTP 409 (Conflict): If a duplicate record is found (username, email, or phone).
        - HTTP 500 (Internal Server Error): For any unexpected errors.
    """
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to register a new user.

        This method:
        - Validates the incoming registration data using the `UserRegistrationSerializer`.
        - Checks if the provided username, email, or phone number already exists in the database.
        - Optionally processes and saves a profile image.
        - Creates a new user if all validation checks pass.

        Args:
            request (Request): The HTTP request object containing user data.

        Returns:
            Response: A response with a status code and message indicating success or failure.

        Raises:
            Exception: If an unexpected error occurs during registration.
        """
        try:
            serializer = UserRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                
                validated_data = serializer.validated_data
                
                profile_image = request.FILES.get('profile_url')
                profile_url = None
               
                response = is_record_exists(username=validated_data['username'], 
                                    phone_no=validated_data['phone_no'],
                                    email=validated_data['email'])
                
                if response:
                    return response

                if profile_image and validated_data.get('username') and validated_data.get('role'):
                    profile_url = save_image(profile_image, 
                                        validated_data.get('username'), 
                                        validated_data.get('role'))

                validated_data['profile_url'] = profile_url
                User.objects.create(**validated_data)

                return custom_response(success=True, 
                                       message="User registered successfully", 
                                       status=201)
            
            else:
                _, error_details = next(iter(serializer.errors.items()))
                error_message = error_details[0]
                return custom_response(success=False, 
                                       message=error_message, 
                                       status=400)
            
        except Exception as e:
            return custom_response(success=False, 
                                   message='Something went wrong', 
                                   status=500)



class Login(View):
    """
    Handles user login by validating credentials, authenticating the user, and generating an access token.
    """
    
    def post(self, request, *args, **kwargs):
        try:
            form_data = request.POST
            user = User.objects.filter(username=form_data['email']).first()

            if not user:
                return custom_response(success=False, message="No user found with these credentials.", status=404)
                        
            authenticate_user = authenticate(request, username=form_data.get('email'), password=form_data.get('password'))

            if authenticate_user is not None:
                access_token = generate_token(authenticate_user)
                
                return JsonResponse({
                    "success": True,
                    "message": 'User logged in successfully',
                    "access_token": access_token.token,
                    "token_type": 'Bearer',
                    "expires_in": (access_token.expires.strftime('%Y-%m-%d %H:%M:%S'))
                }, status=200)
            
            else:
                return JsonResponse({
                    "success": False, 
                    "message": "Invalid username or password"
                }, status=400)

        except Exception as e:
            return JsonResponse({
                "success": False, 
                "message": "Something went wrong"
            }, status=500)
