import uuid
from common_app.models import User
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from utils.utils import create_response, create_user
from users.serializer.register_serializer import UserRegistrationSerializer 

class PackageProvider(APIView):
    """
    API view to manage package provider registration.

    This class facilitates the registration of package providers under a specific 
    creator, who must have the role of `package_admin`. It validates the creator's 
    role, ensures input data integrity using a serializer, and delegates the user 
    creation process to a utility function.
    """
    def post(self, request: Request, creator_id: uuid.UUID) -> Response:
        """
        Handles POST requests for package provider registration.

        This method:
        - Validates the creator's existence and role (`package_admin`).
        - Uses `UserRegistrationSerializer` to validate the incoming data.
        - Delegates the creation of the package provider to the `create_user` utility function.

        Args:
            request (Request): The HTTP request object containing package provider registration details.
            creator_id (uuid.UUID): The UUID of the user initiating the creation request, 
            who must have a `package_admin` role.

        Returns:
            Response: A JSON response with a status code and message.
            - HTTP 201: Package provider registered successfully.
            - HTTP 400: Validation errors in the input data.
            - HTTP 404: Creator not found or invalid role.
            - HTTP 500: Unexpected error during registration.
        """
        try:
            creator = User.objects.filter(id=creator_id).first()

            if not creator or creator.role_id.name != 'package_admin':
                return create_response(
                    success=False,  
                    message='Creator not found or in-valid Creator role.',
                    status=404
                )
            
            serializer = UserRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                
                validated_data = serializer.validated_data
                profile_image = request.FILES.get('profile_url')
                
                return create_user(validated_data=validated_data, 
                        profile_image=profile_image,
                        creator_id=creator_id
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
        

