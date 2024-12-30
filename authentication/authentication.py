from django.contrib.auth.models import User
from common_app.models import User, OAuthAccessToken
from django.contrib.auth.backends import BaseBackend

class OAuthBackend(BaseBackend):
    """
    A custom authentication backend for authenticating users via email and password.

    This class provides methods for:
    - Authenticating users based on their email and password.
    - Retrieving user objects by their unique ID.

    """

    def authenticate(email, password):
        """
        Authenticates a user using their email and password.

        This method performs the following steps:
        - Fetches the user with the given email.
        - Validates the provided password against the user's stored password.
        - Returns the user object if authentication is successful.

        Args:
            email (str, optional): The email address of the user trying to authenticate.
            password (str, optional): The password of the user trying to authenticate.

        Returns:
            User or JsonResponse:
                - Returns a User object if authentication is successful.
                - Returns a JsonResponse with an appropriate error message if authentication fails.

        """
        try:
            user = User.objects.filter(email=email).first()
            if not user:
                return None
            
            validate_user = user.check_password(password)

            if not validate_user:
                return None
            
            return user
        
        except OAuthAccessToken.DoesNotExist:
            return None


    def get_user(self, user_id):
        """
        Retrieves a user object by their ID.

        This method attempts to fetch the user with the provided ID from the database.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            User or None:
                - Returns a User object if a user with the given ID exists.
                - Returns None if no user is found.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        

        