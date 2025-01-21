import uuid
from django.utils.timezone import now
from rest_framework.views import APIView
from common_app.models import VehicleType
from rest_framework.request import Request
from rest_framework.response import Response
from package_provider.models import TourPackageBid, TourPackage
from utils.utils import create_response, validate_package_provider_roles, get_user_by_id, check_permissions, update_record
from package_provider.serializer.tour_package_bid_serializer import TourPackageNecessitySerializer, TourPackageAcceptSerializer

class TourPackageBidManagement(APIView):
    """
    API view to manage package provider registration.

    This class facilitates the registration of package providers under a specific 
    creator, who must have the role of `package_admin`. It validates the creator's 
    role, ensures input data integrity using a serializer, and delegates the user 
    creation process to a utility function.
    """


    def get(self, request:Request, 
            user_id: uuid.UUID,
            package_bid_id: uuid.UUID=None,
            ) -> Response:
        try:

            user = get_user_by_id(user_id=user_id)

            if not user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )
            
            user_permission = check_permissions(user=user, permission_type='write')

            if user_permission:
                return user_permission
            
            validate_role = validate_package_provider_roles(user)

            if validate_role:
                return validate_role
            
            if package_bid_id:
                package_necessity = TourPackageBid.objects.filter(id=package_bid_id).values().first()

                if not package_necessity:
                    return create_response(
                        success=False,
                        message="Package requirement not found.",
                        data=[],
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='Retrieved Package requirement successfully.',
                    data=package_necessity,
                    status=200
                )
            

            else:
                package_necessities = TourPackageBid.objects.values().all()

                if not package_necessities:
                    return create_response(
                        success=False,
                        message="Package requirement not found.",
                        data=[],
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='Retrieved Packages requirement successfully.',
                    data=list(package_necessities),
                    status=200
                )

        except:
            return create_response(
                success=False,
                message='Something went wrong',
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
            
            user_permission = check_permissions(user=user, permission_type='write')

            if user_permission:
                return user_permission
            
            validate_role = validate_package_provider_roles(user)

            if validate_role:
                return validate_role
            
            serializer = TourPackageNecessitySerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                if 'vehicle_type_id' not in validated_data.keys():
                    return create_response(
                        success=False,
                        message='vehicle_type_id is missing.',
                        status=404
                    )
                
                if 'tour_package_id' not in validated_data.keys():
                    return create_response(
                        success=False,
                        message='tour_package_id is missing.',
                        status=404
                    )

                validate_bidding = TourPackageBid.objects.filter(tour_package_id=validated_data['tour_package_id']).first()

                if validate_bidding:
                    return create_response(
                        success=False,
                        message='Package requirement already exist',
                        status=409
                    )
                
                validated_data['vehicle_type_id'] = VehicleType.objects.filter(id=validated_data['vehicle_type_id']).first()
                validated_data['tour_package_id'] = TourPackage.objects.filter(id=validated_data['tour_package_id']).first()
                
                TourPackageBid.objects.create(**validated_data)
                return create_response(
                    success=True,
                    message='Package requirement create.',
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
        

    def put(self, request:Response, 
            package_bid_id: uuid.UUID,
            user_id: uuid.UUID
        ) -> Response :
        try:
            user = get_user_by_id(user_id=user_id)

            if not user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )
            
            user_permission = check_permissions(user=user, permission_type='write')

            if user_permission:
                return user_permission
            
            validate_role = validate_package_provider_roles(user)

            if validate_role:
                return validate_role
            
            serializer = TourPackageNecessitySerializer(data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                if 'vehicle_type_id' in validated_data.keys():
                    validated_data['vehicle_type_id'] = VehicleType.objects.filter(id=validated_data['vehicle_type_id']).first()
                
                if 'tour_package_id' in validated_data.keys():
                    validated_data['tour_package_id'] = TourPackage.objects.filter(id=validated_data['tour_package_id']).first()

                TourPackageNecessityObject = TourPackageBid.objects.filter(id=package_bid_id).first()

                if not TourPackageNecessityObject:
                    return create_response(
                        success=False,
                        message='Package requirement not found',
                        status=409
                    )
                
                update_record(TourPackageNecessityObject, validated_data)
                
                TourPackageNecessityObject.save()
                return create_response(
                    success=True,
                    message='Package requirement update.',
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


    def delete(self, request: Request, 
            package_bid_id: uuid.UUID,
            user_id: uuid.UUID
        ) -> Response :
        try:
            user = get_user_by_id(user_id=user_id)

            if not user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )

            user_permission = check_permissions(user=user, permission_type='write')

            if user_permission:
                return user_permission

            validate_role = validate_package_provider_roles(user)

            if validate_role:
                return validate_role
            
            TourPackageNecessityObject = TourPackageBid.objects.filter(id=package_bid_id).first()

            if not TourPackageNecessityObject:
                return create_response(
                    success=False,
                    message='Package requirement not found.',
                    status=404
                )

            TourPackageNecessityObject.delete()
            return create_response(
                success=True,
                message='Package requirement deleted',
                status=200
            )

        except: 
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )



class TourPackageAccept(APIView):

    def put(self, request: Request,
            package_bid_id: uuid.uuid4,
            user_id: uuid.uuid4,
        ):
        
        try:
            user = get_user_by_id(user_id=user_id)

            if not user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )

            user_permission = check_permissions(user=user, permission_type='write')

            if user_permission:
                return user_permission

            validate_role = validate_package_provider_roles(user)

            if validate_role:
                return validate_role
        
            TourPackageBidObject = TourPackageBid.objects.filter(id=package_bid_id).first()

            if not TourPackageBidObject:
                return create_response(
                    success=False,
                    message='Package requirement not found.',
                    status=404
                )
            
            elif TourPackageBidObject.bid_status == 'accepted':
                return create_response(
                    success=False,
                    message='Package already accepted.',
                    status=404
                )
            

            serializer = TourPackageAcceptSerializer(data=request.data)

            if serializer.is_valid():

                validated_data = serializer.validated_data

                TourPackageBidObject.approved_proposal_id = validated_data['approved_proposal_id']
                TourPackageBidObject.proposal_approved_at = now()
                TourPackageBidObject.bid_status = 'accepted'

                TourPackageBidObject.save()
                return create_response(
                    success=True,
                    message='Bid accepted.',
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