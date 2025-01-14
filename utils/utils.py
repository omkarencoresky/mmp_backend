import os
import uuid
import redis
import pyotp
import secrets
import datetime

from functools import wraps
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client
from datetime import timedelta
from common_app.models import *
from django.conf import settings
from django.http import JsonResponse
from django.http import JsonResponse
from twilio.base.exceptions import TwilioRestException
from common_app.models import OAuthAccessToken, OAuthApplication


load_dotenv()

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

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
    if data:
        response_data["data"] = data

    return JsonResponse(
        response_data, 
        status=status
    )


def save_image(uploaded_image, user_id: uuid.UUID, role: str):
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

    extension = uploaded_image.name.split('.')[-1].lower()
    folder_path = os.path.join(settings.BASE_DIR, 'media', role)
    
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{user_id}_image.{extension}"
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'wb+') as f:
        for chunk in uploaded_image.chunks():
            f.write(chunk)

    return os.path.join(settings.MEDIA_URL, role, filename)
    
    

def image_extension_validator(profile_image):

    allowed_extension = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
    extension = profile_image.name.split('.')[-1].lower()

    if extension not in allowed_extension:
        return create_response(
            success=False,
            message='Profile image format In-valid.',
            status=404
        )
    return None


def create_user(validated_data, profile_image=None, user_id=None):
    """
    Handles user creation with validation, role assignment, and optional profile image processing.

    Args:
        validated_data (dict): The validated data for creating the user, including phone_no, email, and role_id.
        profile_image (InMemoryUploadedFile, optional): The uploaded profile image file for the user. Defaults to None.

    Returns:
        Response: A JSON response with a status code and message.
        - HTTP 201: User successfully created.
        - HTTP 409: Duplicate username, email, or phone number.
        - HTTP 500: Internal server error.
    """
    try:
        response = is_record_exists(
            phone_no=validated_data['phone_no'],
            email=validated_data['email']
        )
        
        if response:
            return response

        role_id = validated_data.get('role_id')
        role = Role.objects.filter(id=role_id).first()
        
        if not role:
            return create_response(
                success=False,
                message='In-valid role.',
                status=404
            )
        
        validated_data['role_id'] = role
        validated_data['created_by'] = get_user_by_id(user_id=user_id)

        user = User.objects.create(**validated_data)

        if profile_image:
            profile_url = save_image(
                uploaded_image=profile_image,
                user_id=user.id,
                role=role.name
            )

            if profile_url:
                user.profile_url = profile_url
        user.save()

        return create_response(
            success=True,
            message="Register successfully.",
            status=201
        )
    
    except Exception as e:
        return create_response(
            success=False,
            message="Something went wrong.",
            status=500
        )
    

def update_user_profile_image(user: User, profile_image) -> str:
    """
    Updates the user's profile image by replacing the old image with the new one.

    This function:
    - Validates the image format.
    - Deletes the old profile image (if it exists).
    - Saves the new profile image and updates the `profile_url`.

    Args:
        user (User): The user object to update.
        profile_image (InMemoryUploadedFile): The uploaded image file.

    Returns:
        str: The URL of the newly saved profile image if successful, or None if failure.
    """

    old_image_path = os.path.join(settings.BASE_DIR, 'media', user.profile_url.replace(settings.MEDIA_URL, '').lstrip('/'))

    if os.path.exists(old_image_path):
        os.remove(old_image_path)

    profile_url = save_image(
        uploaded_image=profile_image,
        role=user.role_id.name,
        user_id=user.id,
    )

    if profile_url:
        user.profile_url = profile_url



def is_email_exist(email: str):
    """
    Checks if an email address exists in the User model.

    Args:
        email (str): The email address to check for existence.

    Returns:
        bool: True if the email exists, False otherwise.
    """
    return User.objects.filter(email=email).exists()


def is_phone_number_exist(phone_no: str, country_code: str=None):
    """
    Checks if a phone number exists in the User model.

    Args:
        phone_no (str): The phone number to check for existence.

    Returns:
        bool: True if the phone number exists, False otherwise.
    """
    if country_code:
        return User.objects.filter(phone_no=phone_no, country_code=country_code).first()
    return User.objects.filter(phone_no=phone_no).first()


def is_user_id_exist(user_id: uuid.UUID):
    """
    Checks if a user with the specified ID exists in the User model.

    Args:
        user_id (int): The ID of the user to check for existence.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    return User.objects.filter(id=user_id).exists()


def is_record_exists(username: str = None, email: str = None, phone_no: str = None):
    """
    Checks if any of the given records (username, email, or phone number) exist in the database.
    
    Args:
        username (str): The username to check.
        email (str): The email to check.
        phone_no (str): The phone number to check.
    
    Returns:
        JsonResponse: A JsonResponse indicating if any record exists, or None if record in not exists.
    """
    
    
    if email:
        email = is_email_exist(email)

        if email:
            return create_response(
                success=False, 
                message="User with this email already exists", 
                status=400
            )

    if phone_no:
        phone_no = is_phone_number_exist(phone_no=phone_no)

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
    
    except Exception:
        return None
    


def retrieve_user_details(user_id: uuid.UUID = None):
    """
    Checks if a user with the specified ID exists in the User model.

    Args:
        user_id (int): The ID of the user to check for existence.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    try:
        if user_id is not None:
            data = User.objects.filter(id=user_id).values(
                        'first_name', 'last_name', 'middle_name', 'email'
                        , 'phone_no', 'gender', 'date_of_birth', 'is_active', 'last_login'
                    ).first()
            return data
        
        else:
            data =  User.objects.values(
                        'first_name', 'last_name', 'middle_name', 'email'
                        , 'phone_no', 'gender', 'date_of_birth', 'is_active', 'last_login'
                    )
            return list(data)

    except Exception:
        return None
    

def fetch_address_details(user_id: uuid.UUID = None, address_id: uuid.UUID = None):
    """
    Checks if a user with the specified ID exists in the User model.

    Args:
        user_id (int): The ID of the user to check for existence.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    try:
        if address_id:
            data = User_Address.objects.filter(id=address_id).values(
                    'id', 'user_id', 'house_no', 'apartment', 'nearest_landmark', 'pin_code', 'user_id', 
                    'street_address', 'city', 'state', 'postal_code', 'country', 'latitude', 'longitude'
                ).first()
            return data
        
        elif user_id:
            data =  User_Address.objects.filter(user_id=user_id).values(
                    'id', 'user_id', 'house_no', 'apartment', 'nearest_landmark', 'pin_code', 'user_id', 
                    'street_address', 'city', 'state', 'postal_code', 'country', 'latitude', 'longitude'
                ).all()
            return list(data)
        
        else:
            data =  User_Address.objects.values(
                    'id', 'user_id', 'house_no', 'apartment', 'nearest_landmark', 'pin_code', 'user_id', 
                    'street_address', 'city', 'state', 'postal_code', 'country', 'latitude', 'longitude'
                ).all()
            return list(data)

    except Exception as e:
        return None
    

def get_user_by_id(user_id: uuid.UUID):
    """
    Checks if a user with the specified ID exists in the User model.

    Args:
        user_id (int): The ID of the user to check for existence.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    return User.objects.filter(id=user_id).first()


def get_address_by_id(address_id: uuid.UUID):
    """
    Checks if a address with the specified ID exists in the User model.

    Args:
        address_id (int): The ID of the address to check for existence.

    Returns:
        bool: True if the address exists, False otherwise.
    """
    return User_Address.objects.filter(id=address_id).first()



def generate_otp(user: uuid.UUID):
    """
    Generate a OTP and store it in Redis.
    
    Args:
    mobile_number (str): The mobile number of the user requesting the OTP.

    Returns:
    str: OTP
    """

    try:
        otp = pyotp.TOTP(pyotp.random_base32()).now()
        redis_key = f"otp:{user.id}"
        redis_client.setex(redis_key, 300, otp)
        return otp
    
    except:
        return None


def verify_otp(user_id: uuid.UUID, otp_input: str):
    """
    Verifies the OTP provided by the user.

    This method:
    - Retrieves and checks the stored OTP from Redis.
    - Deletes the OTP if verified.

    Args:
        user_id (uuid.UUID): The user's unique ID.
        otp_input (str): The OTP entered by the user.

    Returns:
        tuple: 
            - (bool): True if valid, False if invalid or expired.
            - (str): Message indicating the result (e.g., success or error).
    """
    redis_key = f"otp:{user_id}"
    stored_otp = redis_client.get(redis_key)
    
    if stored_otp is None:
        return False, "OTP expired.", 410
    
    if stored_otp == otp_input:
        # OTP is valid
        redis_client.delete(redis_key)
        return True, "OTP verified successfully.", 200
    
    return False, "Invalid OTP.", 409



def send_otp(country_code: str, phone_no: str, otp: str):
    """
    Generate a OTP and store it in Redis.
    
    Args:
    mobile_number (str): The mobile number of the user requesting the OTP.

    Returns:
    str: OTP
    """
    try:
        account_sid = os.getenv('TWILIO_SID')
        auth_token = os.getenv('TWILIO_TOKEN')

        client = Client(account_sid, auth_token)
        client.messages.create(
            to=f"{country_code}{phone_no}",
            from_="+1 218 506 1882",
            body=f"Your OTP for login is {otp}. It is valid for 5 minutes."
        )
        return otp
    
    except TwilioRestException as e:
        print(e)

    except:
        return None
    

def update_record(object, data: dict):
    """
    Updates the attributes of a given object using a dictionary of key-value pairs.

    Parameters:
        object: Any
            The object whose attributes are to be updated.
        data (dict): A dictionary where the keys are the attribute names (as strings) 
                    and the values are the new values to assign to those attributes.

    Returns:
        bool: 
            - `True` if all attributes were successfully updated.
            - `False` if an exception occurs during the update process.
    """
    if data.get('email') and User.objects.filter(email=data['email']).exclude(email=object.email).exists():
        return False, 'Email is already exist.', 409
    
    if data.get('phone_no') and User.objects.filter(phone_no=data['phone_no']).exclude(phone_no=object.phone_no).exists():
        return False, 'Phone number is already exist.', 409

    for field, value in data.items():
            setattr(object, field, value)
    # return True, 'Updated', 200

    

def check_permissions(user, permission_type:str):
    """
    Check if a user has the required permission for a specific action.

    This function checks the permissions associated with the user's role 
    to determine if the user is allowed to perform the specified action.

    Args:
        user (User): The user object for which the permission is being checked.
        permission_type (str): The type of permission required (e.g., 'read', 'write', 'update', 'delete').

    Returns:
        Response:
            - A `Response` object with an error message and status 404 if the permission is denied.
        bool:
            - `False` if an exception occurs during the process.
            - If permission is allowed, the function implicitly returns `None`.
    """
        
    try:

        role_permission = Permission.objects.filter(role_id= user.role_id).first()
        
        if permission_type not in role_permission.permission.split(','):
            return create_response(
                success=False,
                message='Permission denied!',
                status=403
            )
        
    except:
        return False
    

def validate_package_provider_roles(user, role_list: list=None):
    """
    Validates the role of a user to ensure they are either a 'package_admin' or 'package_sub_admin'.
    
    This function checks the role of the provided user and returns a response indicating
    whether the user's role is valid or not. If the user's role is not one of the allowed roles 
    ('package_admin' or 'package_sub_admin'), the function returns a response with an error message.
    
    Args:
        user (User): A user object that contains the user's role information.
    
    Returns:
        dict or bool: A response dictionary containing the success status, message, and HTTP status
        code if the validation fails, or False if an error occurs during validation.
    """
    
    try:

        if role_list is None:
            role_list = ['package_admin', 'package_sub_admin']
        
        if user.role_id.name not in role_list:
            return create_response(
                success=False,
                message='Invalid role.',
                status=401
            )

    except:
        return False
    


def validate_travel_agency_roles(user, role_list: list=None):
    """
    Validates the role of a user to ensure they are either a 'travel_admin' or 'travel_sub_admin'.
    
    This function checks the role of the provided user and returns a response indicating
    whether the user's role is valid or not. If the user's role is not one of the allowed roles 
    ('travel_admin' or 'travel_sub_admin'), the function returns a response with an error message.
    
    Args:
        user (User): A user object that contains the user's role information.
    
    Returns:
        dict or bool: A response dictionary containing the success status, message, and HTTP status
        code if the validation fails, or False if an error occurs during validation.
    """
    
    try:

        if role_list is None:
            role_list = ['travel_admin', 'travel_sub_admin']

        if user.role_id.name not in role_list:
            return create_response(
                success=False,
                message='Invalid role.',
                status=401
            )

    except:
        return False
    

def validate_roles_for_company(user):
    """
    Validates the role of a user to ensure they are either a 'travel_admin' or 'package_admin'.
    
    This function checks the role of the provided user and returns a response indicating
    whether the user's role is valid or not. If the user's role is not one of the allowed roles 
    ('travel_admin' or 'package_admin'), the function returns a response with an error message.
    
    Args:
        user (User): A user object that contains the user's role information.
    
    Returns:
        dict or bool: A response dictionary containing the success status, message, and HTTP status
        code if the validation fails, or False if an error occurs during validation.
    """
    
    try:

        if user.role_id.name not in ['travel_admin', 'package_admin']:
            return create_response(
                success=False,
                message='Invalid role.',
                status=401
            )

    except:
        return False


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