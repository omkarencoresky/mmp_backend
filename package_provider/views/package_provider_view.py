from utils.utils import create_response
from rest_framework.views import APIView
from common_app.models import User, User_Address

class PackageProvider(APIView):
    def post(self, request, creater_id):
        try:
            creater = User.objects.filter(id=creater_id).first()
            if creater and creater.role == 'package_admin':
                
            
                pass
        except:
            return create_response(
                success=False,
                message="Something went wrong!",
                status=500
            )