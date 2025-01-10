import uuid

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from package_provider.models import DailyItinerary, TourPackage
from package_provider.serializer.daily_itinerary_serializer import DailyItinerarySerializer
from utils.utils import  get_user_by_id, validate_package_provider_roles, check_permissions, create_response, update_record

class DailyItineraryManagement(APIView):

    """
    APIView for managing Daily itinerary.

    API View for managing daily itineraries in tour packages, providing endpoints to retrieve
    (GET), create (POST), update (PUT), and delete (DELETE) itineraries. This ensures seamless
    management of itinerary data for tour packages. 
    """

    def get(self, request: Request, 
            user_id: uuid.UUID,
            package_id: uuid.UUID=None,
            itinerary_id: uuid.UUID=None
        ) -> Response:
        
        """
        Retrieve daily itineraries for a specific package or details of a specific itinerary.

        Args:
            request (Request): The incoming HTTP request.
            user_id (uuid.UUID): The ID of the user making the request.
            package_id (uuid.UUID, optional): The ID of the package for which itineraries are retrieved.
            itinerary_id (uuid.UUID, optional): The ID of the specific itinerary to retrieve.

        Returns:
            Response: A JSON response with the itinerary data or an error message.
        """

        try:

            user = get_user_by_id(user_id=user_id)

            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )

            validate_role = validate_package_provider_roles(user=user)

            if validate_role:
                return validate_role

            permission = check_permissions(user=user, permission_type='read')

            if permission:
                return permission

            if package_id:

                itinerary_list = DailyItinerary.objects.filter(package_id=package_id).values().all()

                if not itinerary_list:
                    return create_response(
                        success=False,
                        message='Itinerary not found',
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='Itinerary list',
                    data=list(itinerary_list),
                    status=200
                )

            else:
                itinerary = DailyItinerary.objects.filter(id=itinerary_id).values().first()

                if not itinerary:
                    return create_response(
                        success=False,
                        message='Itinerary not found',
                        status=404
                    )

                return create_response(
                    success=True,
                    message='Itinerary details',
                    data=itinerary,
                    status=200
                )

        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )


    def post(self, request: Request, 
            user_id: uuid.UUID,
            package_id: uuid.UUID,
        ) -> Response:

        """
        Create a new daily itinerary for a specific package.

        Args:
            request (Request): The incoming HTTP request with itinerary data.
            user_id (uuid.UUID): The ID of the user making the request.
            package_id (uuid.UUID): The ID of the package to associate the itinerary with.

        Returns:
            Response: A JSON response with the status of the operation.
        """
        
        try:
            user = get_user_by_id(user_id=user_id)
            package = TourPackage.objects.filter(id=package_id).first()
            
            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            validate_role = validate_package_provider_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='write')
            
            if permission:
                return permission
            
            serializer = DailyItinerarySerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                tour_package_instance = DailyItinerary.objects.filter(package_id=package_id, **validated_data)

                if tour_package_instance:
                    return create_response(
                        success=False,
                        message='Itinerary already exist',
                        status=404
                    )
                
                DailyItinerary.objects.create(package_id=package, **validated_data)

                return create_response(
                    success=True,
                    message='Itinerary created.',
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
        
        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )
        
    def put(self, request: Request, 
            user_id: uuid.UUID,
            itinerary_id: uuid.UUID
        ) -> Response:
        
        """
        Update an existing daily itinerary.

        Args:
            request (Request): The incoming HTTP request with updated itinerary data.
            user_id (uuid.UUID): The ID of the user making the request.
            itinerary_id (uuid.UUID): The ID of the itinerary to update.

        Returns:
            Response: A JSON response with the status of the operation.
        """
        
        try:
            user = get_user_by_id(user_id=user_id)
            
            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            validate_role = validate_package_provider_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='update')
            
            if permission:
                return permission

            serializer = DailyItinerarySerializer(data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                itinerary = DailyItinerary.objects.filter(id=itinerary_id).first()

                update_itinerary = update_record(itinerary, validated_data)

                if not update_itinerary:
                    return create_response(
                        success=False,
                        message='Something went wrong.',
                        status=500
                    )
                
                itinerary.save()
                return create_response(
                    success=True,
                    message='Itinerary update',
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

        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )
        

    def delete(self, request: Request, 
            user_id: uuid.UUID,
            itinerary_id: uuid.UUID
        ) -> Response:
        
        """
        Delete a specific daily itinerary.

        Args:
            request (Request): The incoming HTTP request.
            user_id (uuid.UUID): The ID of the user making the request.
            itinerary_id (uuid.UUID): The ID of the itinerary to delete.

        Returns:
            Response: A JSON response with the status of the operation.
        """
        
        try:

            user = get_user_by_id(user_id=user_id)
            
            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            validate_role = validate_package_provider_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='delete')
            
            if permission:
                return permission

            itinerary = DailyItinerary.objects.filter(id=itinerary_id).first()

            if not itinerary:
                return create_response(
                    success=False,
                    message='Itinerary not found',
                    status=404
                )
            
            itinerary.delete()
            return create_response(
                success=True,
                message='Itinerary delete',
                status=204
            )

        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )