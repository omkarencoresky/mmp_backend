import os
from django.conf import settings
from common_app.models import User
from django.http import JsonResponse
from django.utils.text import slugify


# from datetime import timedelta
# from django.conf import settings
# from django.utils import timezone
# from oauth2_provider.models import Application
# from oauth2_provider.models import AccessToken
# from oauth2_provider.models import RefreshToken
# from django.utils.crypto import get_random_string
# from django.core.exceptions import ValidationError
# from oauth2_provider.settings import oauth2_settings
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User as builtin_User

def custom_response(success: bool = None, message: str = None, data: JsonResponse = None, status: int = None) -> JsonResponse:
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
    if data is not None:
        response_data["data"] = data

    return JsonResponse(response_data, status=status)


def save_image(uploaded_image, username: str, role: str):
    """
    Saves the uploaded profile image to the server in a role-specific directory and returns the URL of the saved image.

    Arguments:
        uploaded_image (file): The uploaded image file to be saved.
        username (str): The username to be used in the file name of the saved image.
        role (str): The role of the user, used to determine the subfolder (e.g., 'driver', 'package_provider', etc.)

    Returns:
        str or None: The URL of the saved profile image if successful, or None if no image is uploaded.
    """
    if not uploaded_image or role not in ["user", "driver", "travel_admin", "package_admin", "travel_sub_admin", 
                                            "package_sub_admin"]:
        return custom_response(success=False, message="Invalid role. Must be one of 'user', 'driver', 'travel_admin', \
                                               'package_admin', 'travel_sub_admin', or 'package_sub_admin'.", status=500)

    try:
        extension = uploaded_image.name.split('.')[-1].lower()
        folder_path = os.path.join(settings.BASE_DIR, 'media', role)
        print('folder_path',folder_path)
        os.makedirs(folder_path, exist_ok=True)

        filename = f"{slugify(username)}_image.{extension}"
        file_path = os.path.join(folder_path, filename)
        print('file_path',file_path)

        with open(file_path, 'wb+') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        return os.path.join(settings.MEDIA_URL, role, filename)
    
    except Exception:
        return custom_response(success=False, message="Error saving profile image", status=500)



def username_exist(username):
    """
    Checks if a username exists in either the PackageProviderUser or builtin_User models.

    Args:
        username (str): The username to check for existence.

    Returns:
        str: Error message if username exists, else None.
    """
    if User.objects.filter(username=username).exists():
        return 'Username is already exist'
    return None


def email_exist(email):
    """
    Checks if an email address exists in either the PackageProviderUser or builtin_User models.

    Args:
        email (str): The email address to check for existence.

    Returns:
        str: Error message if email exists, else None.
    """
    if User.objects.filter(email=email).exists():
        return 'Email is already exist'
    return None


def phone_number_exist(phone_no):
    """
    Checks if a phone number exists in the PackageProviderUser model.

    Args:
        phone_no (str): The phone number to check for existence.

    Returns:
        str: Error message if phone number exists, else None.
    """
    if User.objects.filter(phone_no=phone_no).exists():
        return 'Phone number is already exist'
    return None


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
        message = username_exist(username)
        if message:
            return custom_response(success=False, message=message, status=400)
    
    if email:
        message = email_exist(email)
        if message:
            return custom_response(success=False, message=message, status=400)

    if phone_no:
        message = phone_number_exist(phone_no)
        if message:
            return custom_response(success=False, message=message, status=400)
    
    return None

