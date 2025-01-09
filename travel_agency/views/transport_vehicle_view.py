import uuid

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from travel_agency.models import TransportVehicle
from travel_agency.serializer.transport_vehicle_serializer import TransportVehicleSerializer
from utils.utils import create_response, get_user_by_id, update_record, validate_travel_agency_roles, check_permissions

class TransportVehicleManagement(APIView): 

    """
    APIView for managing transport vehicles in a travel agency system.

    This class provides methods for CRUD operations on transport vehicles,
    including retrieving vehicle details or a list of vehicles, adding a new
    vehicle, updating existing vehicle details, and deleting a vehicle.
    User roles and permissions are validated before performing any operation.
    
    """

    def get(self, request: Request, 
            user_id: uuid.UUID, 
            transport_vehicle_id: uuid.UUID=None,
        ) -> Response:

        """
        Retrieve transport vehicle details or a list of vehicles for a user.

        Args:
            request (Request): The request object containing user and query parameters.
            user_id (uuid.UUID): The ID of the user whose vehicles are being queried.
            transport_vehicle_id (uuid.UUID, optional): The ID of the specific vehicle to retrieve.

        Returns:
            Response: 
                - 200: Success with vehicle details or list of vehicles.
                - 404: Vehicle not found or no vehicles associated with the user.
                - 500: Internal server error.
        """

        try:

            user = get_user_by_id(user_id=user_id)
            validate_role = validate_travel_agency_roles(user=user)

            if validate_role:
                return validate_role

            permission = check_permissions(user=user, permission_type='read')
            
            if permission:
                return permission
            
            if transport_vehicle_id:
                transport_vehicle = TransportVehicle.objects.filter(id=transport_vehicle_id).values().first()

                if not transport_vehicle:
                    return create_response(
                        success=False,
                        message='Vehicle not found.',
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='Vehicle details.',
                    data=transport_vehicle,
                    status=200
                )
            
            else:
                transport_vehicle_list = TransportVehicle.objects.filter(user_id=user_id).values().all()

                if not transport_vehicle_list:
                    return create_response(
                        success=False,
                        message='Vehicle not found.',
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='Vehicles details list.',
                    data=list(transport_vehicle_list),
                    status=200
                )

        except:
            return create_response(
                success=False,
                message="Something went wrong!",
                status=500
            )
        
    
    def post(self, request: Request, 
            user_id: uuid.UUID,
        ) -> Response:

        """
        Add a new transport vehicle to the system.

        Args:
            request (Request): The request object containing transport vehicle details.
            user_id (uuid.UUID): The ID of the user adding the vehicle.

        Returns:
            Response: 
                - 201: Vehicle successfully added.
                - 400: Validation error with vehicle data.
                - 404: User not found.
                - 500: Internal server error.
        """

        try:
            user = get_user_by_id(user_id=user_id)

            if not user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )
            
            validate_role = validate_travel_agency_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='write')
            
            if permission:
                return permission
            
            serializer = TransportVehicleSerializer(data=request.data)

            if serializer.is_valid():
                
                validated_data = serializer.validated_data

                tour_package_instance = TransportVehicle.objects.filter(user_id=user, **validated_data)

                if tour_package_instance:
                    return create_response(
                        success=False,
                        message='Vehicle already exist.',
                        status=404
                    )
                
                TransportVehicle.objects.create(user_id=user, **validated_data)

                return create_response(
                    success=True,
                    message='Vehicle Added.',
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
                message="Something went wrong!",
                status=500
            )
        
    
    def put(self, request: Request, 
            user_id: uuid.UUID=None, 
            transport_vehicle_id: uuid.UUID=None,
        ) -> Response:

        """
        Update details of an existing transport vehicle.

        Args:
            request (Request): The request object containing updated vehicle details.
            user_id (uuid.UUID, optional): The ID of the user updating the vehicle.
            transport_vehicle_id (uuid.UUID, optional): The ID of the vehicle to update.

        Returns:
            Response: 
                - 201: Vehicle successfully updated.
                - 400: Validation error with updated data.
                - 404: Vehicle not found.
                - 500: Internal server error.
        """

        try:
            transport_vehicle = TransportVehicle.objects.filter(id=transport_vehicle_id).first()
            user = get_user_by_id(user_id=user_id)

            if not transport_vehicle:
                return create_response(
                    success=False,
                    message='Vehicle not found.',
                    status=404
                )   
            
            validate_role = validate_travel_agency_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='update')
            
            if permission:
                return permission
            
            serializer = TransportVehicleSerializer(data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                transport_vehicle_instance = update_record(transport_vehicle, validated_data)

                if not transport_vehicle_instance:
                    return create_response(
                        success= False,
                        message='Something went wrong.',
                        status=500
                    )
                
                return create_response(
                    success=True,
                    message='Vehicle updated.',
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
                message="Something went wrong!",
                status=500
            )
        

    def delete(self, request: Request, 
            user_id: uuid.UUID=None, 
            transport_vehicle_id: uuid.UUID=None,
        ) -> Response:

        """
        Delete a transport vehicle from the system.

        Args:
            request (Request): The request object.
            user_id (uuid.UUID, optional): The ID of the user deleting the vehicle.
            transport_vehicle_id (uuid.UUID, optional): The ID of the vehicle to delete.

        Returns:
            Response: 
                - 204: Vehicle successfully deleted.
                - 404: Vehicle not found.
                - 500: Internal server error.
        """

        try:
            transport_vehicle = TransportVehicle.objects.filter(id=transport_vehicle_id).first()
            user = get_user_by_id(user_id=user_id)

            if not transport_vehicle:
                return create_response(
                    success=False,
                    message='Vehicle not found.',
                    status=404
                    )
            
            validate_role = validate_travel_agency_roles(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='delete')
            
            if permission:
                return permission
            
            transport_vehicle.delete()
            return create_response(
                success=True,
                message='Vehicle deleted.',
                status=204
            )

        except:
            return create_response(
                success=False,
                message="Something went wrong!",
                status=500
            )