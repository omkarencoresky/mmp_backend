import uuid

from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from common_app.models import BidProposal
from common_app.serializer.bidding_proposal_serializer import TourPackageBidSerializer
from utils.utils import create_response, get_user_by_id, check_permissions, validate_roles_for_admin, update_record



class PackageProposalManagement(APIView):

    def get(self, request: Request, 
            user_id: uuid.UUID,
            bid_id: uuid.UUID=None,
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
            
            validate_role = validate_roles_for_admin(user)

            if validate_role:
                return validate_role

            if bid_id:
                bid = BidProposal.objects.filter(id=bid_id).values().first()

                if not bid:
                    return create_response(
                        success=False,
                        message='Bid not found.',
                        data=[],
                        status=404
                    )

                return create_response(
                    success=True,
                    message='Retrieved Bid detail.',
                    data=bid,
                    status=200
                )

            else:
                biddings = BidProposal.objects.values().all()

                if not biddings:
                    return create_response(
                        success=False,
                        message='Bid not found.',
                        data=[],
                        status=404
                    )

                return create_response(
                    success=True,
                    message='Retrieved bid details.',
                    data=list(biddings),
                    status=200
                )

        except:
            return create_response(
                success=False,
                message='Something went wrong.' ,
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

            validate_role = validate_roles_for_admin(user)

            if validate_role:
                return validate_role

            serializer = TourPackageBidSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                validate_bidding = BidProposal.objects.filter(bid_id=validated_data['bid_id'], travel_agency_id=validated_data['travel_agency_id']).first()

                if validate_bidding:
                    return create_response(
                        success=False,
                        message='Bid already exist',
                        status=409
                    )

                BidProposal.objects.create(**validated_data)
                return create_response(
                    success=True,
                    message='Bid create.',
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
            bid_id: uuid.UUID=None,
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

            validate_role = validate_roles_for_admin(user)

            if validate_role:
                return validate_role

            serializer = TourPackageBidSerializer(data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                TourPackageBidObject = BidProposal.objects.filter(id=bid_id).first()

                if not TourPackageBidObject:
                    return create_response(
                        success=False,
                        message='Bid not found.',
                        status=404
                    )

                update_record(TourPackageBidObject, validated_data)
                
                TourPackageBidObject.save()
                return create_response(
                    success=True,
                    message='Bid updated.',
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
            user_id: uuid.UUID,
            bid_id: uuid.UUID=None,
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
            
            validate_role = validate_roles_for_admin(user)

            if validate_role:
                return validate_role
            
            TourPackageBidObject = BidProposal.objects.filter(id=bid_id).first()

            if not TourPackageBidObject:
                return create_response(
                    success=False,
                    message='Bid not found.',
                    status=404
                )

            TourPackageBidObject.delete()
            return create_response(
                success=True,
                message='Bid deleted.',
                status=201
            )

        except:
            return create_response(
                success=False,
                message='Something went wrong.' ,
                status=500
            )