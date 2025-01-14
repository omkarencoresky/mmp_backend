import uuid
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from common_app.models import TourPackageBid
from utils.utils import create_response, get_user_by_id, check_permissions



class TourPackageBidManagement(APIView):

    def get(self, request: Request) -> Response:
        try:
            pass

        except:
            return create_response(
                success=False,
                message='Something went wrong.' ,
                status=500
            )
        

    def post(self, request: Request, user_id: uuid.UUID) -> Response:
        try:
            grant_user = get_user_by_id(user_id=user_id)

            if not grant_user:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )
            
            user_permission = check_permissions(user=grant_user, permission_type='write')

            if user_permission:
                return user_permission

        except:
            return create_response(
                success=False,
                message='Something went wrong.' ,
                status=500
            )
        
    def put(self, request: Request) -> Response:
        try:
            pass

        except:
            return create_response(
                success=False,
                message='Something went wrong.' ,
                status=500
            )
        

    def delete(self, request: Request) -> Response:
        try:
            pass

        except:
            return create_response(
                success=False,
                message='Something went wrong.' ,
                status=500
            )