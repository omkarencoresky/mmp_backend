import os
import secrets
import datetime

from functools import wraps
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.http import JsonResponse
from django.http import JsonResponse
from django.utils.text import slugify
from common_app.models import OAuthAccessToken
from common_app.models import User, User_Address
from common_app.models import OAuthAccessToken, OAuthApplication


def create_response(success: bool = None, message: str = None, data: JsonResponse = None, 
                    status: int = None) -> JsonResponse:
    """
    Generates a JsonResponse with the given success flag, message, and HTTP status code.

    Args:
        success (bool): A flag indicating whether the request was successful or not.
        message (str): A message to be included in the response.
        status (int): The HTTP status code to be returned with the response.

    Returns:
        JsonResponse: A JsonResponse object containing the success flag, message, and status code.
    """

    response_data = {
        "success": success,
        "message": message
    }
    if not data:
        response_data["data"] = data

    return JsonResponse(
        response_data, 
        status=status
    )


def save_image(uploaded_image, username: str, role: str):
    """
    Saves the uploaded profile image to the server in a role-specific directory and 
        returns the URL of the saved image.

    Arguments:
        uploaded_image (file): The uploaded image file to be saved.
        username (str): The username to be used in the file name of the saved image.
        role (str): The role of the user, used to determine the subfolder (e.g., 'driver', 
            'package_provider', etc.)

    Returns:
        str or None: The URL of the saved profile image if successful, or None if no 
            image is uploaded.
    """

    try:
        extension = uploaded_image.name.split('.')[-1].lower()
        folder_path = os.path.join(settings.BASE_DIR, 'media', role)
        
        os.makedirs(folder_path, exist_ok=True)

        filename = f"{slugify(username)}_image.{extension}"
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'wb+') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        return os.path.join(settings.MEDIA_URL, role, filename)
    
    except Exception:
        return None


def is_username_exist(username):
    """
    Checks if a username exists in the User model.

    Args:
        username (str): The username to check for existence.

    Returns:
        bool: True if the username exists, False otherwise.
    """
    return User.objects.filter(username=username).exists()


def is_email_exist(email):
    """
    Checks if an email address exists in the User model.

    Args:
        email (str): The email address to check for existence.

    Returns:
        bool: True if the email exists, False otherwise.
    """
    return User.objects.filter(email=email).exists()


def is_phone_number_exist(phone_no):
    """
    Checks if a phone number exists in the User model.

    Args:
        phone_no (str): The phone number to check for existence.

    Returns:
        bool: True if the phone number exists, False otherwise.
    """
    return User.objects.filter(phone_no=phone_no).exists()


def is_user_id_exist(user_id):
    """
    Checks if a user with the specified ID exists in the User model.

    Args:
        user_id (int): The ID of the user to check for existence.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    return User.objects.filter(id=user_id).exists()


def is_record_exists(username=None, email=None, phone_no=None):
    """
    Checks if any of the given records (username, email, or phone number) exist in the database.
    
    Args:
        username (str): The username to check.
        email (str): The email to check.
        phone_no (str): The phone number to check.
    
    Returns:
        JsonResponse: A JsonResponse indicating if any record exists, or None if record in not exists.
    """
    
    if username:
        username = is_username_exist(username)

        if username:
            return create_response(
                success=False, 
                message="User with this username already exists", 
                status=400
            )
    
    if email:
        email = is_email_exist(email)

        if email:
            return create_response(
                success=False, 
                message="User with this email already exists", 
                status=400
            )

    if phone_no:
        phone_no = is_phone_number_exist(phone_no)

        if phone_no:
            return create_response(
                success=False, 
                message="User with this phone number already exists", 
                status=400
            )
    
    return None


def generate_token(user):
    """
    Generates a secure access token for the authenticated user and stores it in the database.

    This function creates a new access token for the provided user. It performs the following:
    - Generates a random access token using the `secrets.token_hex` method.
    - Sets an expiration time for the token, which is one hour from the current time.
    - Retrieves client details associated with the OAuth application.
    - Creates or updates an OAuth access token record for the user in the database, 
        ensuring that the token is securely stored.

    Args:
        user (User): The user object for whom the access token is being generated. 
            This user must be authenticated.

    Returns:
        OAuthAccessToken: The generated or updated OAuth access token object, which contains:
            - The access token value (`access_token`).
            - The expiration date and time (`expires_at`).
            - The type of token, which is always set to `'Bearer'` (`token_type`).
    """
    try:
        access_token = secrets.token_hex(32)
        expires_at = datetime.now() + timedelta(hours=1)
        client_details = OAuthApplication.objects.get(id=1)

        token, _ = OAuthAccessToken.objects.update_or_create(
            user=user,
            client=client_details,
            defaults={
                'access_token': access_token,
                'expires_at': expires_at,
                'token_type': 'Bearer',
            }
        )
        return token
    
    except OAuthApplication.DoesNotExist:
        return None
    
    except Exception as e:
        return None
    


def retrieve_user_details(user_id=None):
    """
    Checks if a user with the specified ID exists in the User model.

    Args:
        user_id (int): The ID of the user to check for existence.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    try:
        if not user_id:
            data = User.objects.filter(id=user_id).values(
                        'username', 'first_name', 'last_name', 'middle_name', 'email'
                        , 'phone_no', 'gender', 'date_of_birth', 'role', 'is_active', 'last_login'
                    ).first()
            return data
        
        else:
            data =  User.objects.filter().values(
                        'username', 'first_name', 'last_name', 'middle_name', 'email'
                        , 'phone_no', 'gender', 'date_of_birth', 'role', 'is_active', 'last_login'
                    ).all()
            return list(data)

    except Exception as e:
        return None
    

def fetch_address_details(user_id=None, address_id=None):
    """
    Checks if a user with the specified ID exists in the User model.

    Args:
        user_id (int): The ID of the user to check for existence.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    try:
        if not address_id:
            data = User_Address.objects.filter(id=address_id).values(
                    'id', 'user_id', 'street_address', 'city', 'state', 'pin_code', 'country'
                ).first()
            return data
        
        if not user_id:
            data =  User_Address.objects.filter(user_id=user_id).values(
                    'id', 'user_id', 'street_address', 'city', 'state', 'pin_code', 'country'
                ).all()
            return list(data)

    except Exception as e:
        return None
    

def get_user_by_id(user_id):
    """
    Checks if a user with the specified ID exists in the User model.

    Args:
        user_id (int): The ID of the user to check for existence.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    return User.objects.filter(id=user_id).first()


def get_address_by_id(address_id):
    """
    Checks if a address with the specified ID exists in the User model.

    Args:
        address_id (int): The ID of the address to check for existence.

    Returns:
        bool: True if the address exists, False otherwise.
    """
    return User_Address.objects.filter(id=address_id).first()



# def token_required(view_func):
#     """
#     Decorator to validate the access token from the Authorization header.
#     """
#     @wraps(view_func)
#     def wrapper(request, args, *kwargs):
#         auth_header = request.META.get('HTTP_AUTHORIZATION')
        
#         if not auth_header:
#             return JsonResponse({
#                 "success": False,
#                 "message": "Authorization header is missing."
#             }, status=401)
        
#         try:
#             token_type, token = auth_header.split()
            
#             if token_type.lower() != 'bearer':
#                 return JsonResponse({
#                     "success": False,
#                     "message": "Invalid token type. Only 'Bearer' tokens are supported."
#                 }, status=401)
            
#             access_token = OAuthAccessToken.objects.get(access_token=token)
            
#             if access_token.expires_at < datetime.now():
#                 return JsonResponse({
#                     "success": False,
#                     "message": "Token has expired."
#                 }, status=401)
            
#             request.user = access_token.user
            
#         except (ValueError, OAuthAccessToken.DoesNotExist):
#             return JsonResponse({
#                 "success": False,
#                 "message": "Invalid or missing token."
#             }, status=401)
        
#         return view_func(request, args, *kwargs)
    
#     return wrapper