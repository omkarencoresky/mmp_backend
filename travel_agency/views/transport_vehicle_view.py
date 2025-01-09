import uuid

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from travel_agency.models import TransportVehicle
from travel_agency.serializer.transport_vehicle_serializer import TransportVehicleSerializer
from utils.utils import create_response, get_user_by_id, update_record, validate_travel_agency_roles, check_permissions

class TransportVehicleManagement(APIView): 

    def get(self, request: Request, 
            user_id: uuid.UUID, 
            transport_vehicle_id: uuid.UUID=None,
        ) -> Response:

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