import uuid
from common_app.models import User
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from package_provider.models import TourPackage
from utils.utils import create_response, get_user_by_id, update_record
from package_provider.serializer.tour_serializer import TourPackageSerializer

class TourPackageManagement(APIView):
    def post(
            self, request: Request, 
            user_id: uuid.UUID
        ) -> Response:
        
        try:
            user = get_user_by_id(user_id=user_id)

            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            serializer = TourPackageSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                tour_package_instance = TourPackage.objects.filter(user_id=user_id, **validated_data)

                if tour_package_instance:
                    return create_response(
                        success=False,
                        message='This package already exist',
                        status=404
                    )
                
                TourPackage.objects.filter(user_id=user_id, **validated_data)

                return create_response(
                    success=True,
                    message='Tour package created.',
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
        
    def get(self, request: Request, 
            package_id: uuid.UUID=None, 
            user_id: uuid.UUID=None
        ) -> Response:
        try:
            if package_id:
                package = TourPackage.objects.filter(id=package_id).first()

                if not package:
                    return create_response(
                        success=False,
                        message='Package not found.',
                        status=404
                    )
                
                return create_response (
                    success=True,
                    message='Packages detail.',
                    data=package,
                    status=200
                )

            if user_id:
                user_packages = TourPackage.objects.filter(user_id=user_id).values().all() 

                if not user_packages:
                    return create_response(
                        success=False,
                        message='No package associated with this user.',
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='User package list.',
                    data=list(user_packages),
                    status=200
                )

        except:
            return create_response(
                success=False,
                message="Something went wrong!",
                status=500
            )
        
    
    def put(self, request: Request, package_id: uuid.UUID) -> Response:

        try:
            package = TourPackage.objects.filter(user_id=package_id).first()

            if not package:
                return create_response(
                    success=False,
                    message='User not found.',
                    status=404
                )
            
            serializer = TourPackageSerializer(data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                package_update = update_record(package, validated_data)

                if not package_update:
                    return create_response(
                        success=False,
                        message='Something went wrong.',
                        status=500
                    )
                
                package.save()

                return create_response(
                    success=True,
                    message='Tour package updated.',
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
                message='Something went wrong.'
                status=500
            )
        

    def delete(self, request: Request, package_id: uuid.UUID) -> Response:
        try:
            package = TourPackage.objects.filter(id=package_id).first()

            if not package:
                return create_response(
                    success=False,
                    message='Tour package not found',
                    status=404
                )
            
            # package.delete()
            return create_response(
                success=True,
                message='Tour package delete.',
                status=204
            )
        
        except:
            return create_response(
                success=False,
                message='Something went wrong.',
                status=500
            )