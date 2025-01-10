import uuid
from common_app.models import Company
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from users.serializer.company_serializer import CompanySerializer
from utils.utils import create_response, get_user_by_id, update_record, validate_roles_for_company, check_permissions

class CompanyManagement(APIView):
    """
    A view that handles CRUD operations for Company objects.

    The CompanyManagement class handles various HTTP requests related to managing company data. 
    It provides functionality for retrieving company details (GET), creating new companies (POST), 
    updating existing company information (PUT), and deleting companies (DELETE). The class ensures 
    validation of incoming data, handles errors gracefully, and provides appropriate responses for 
    different scenarios, such as when a company or user is not found. It interacts with the Company 
    model and uses serializers for data validation, offering a structured API for managing company 
    records.
    """

    def get(self, request: Request, 
            user_id: uuid.UUID=None,
            company_id: uuid.UUID=None, 
        ) -> Response:
        """
        Handles GET requests to fetch company details.

        This method:
        - Fetches a single company's details if `company_id` is provided.
        - Fetches a list of companies associated with a `user_id` if `user_id` is provided.
        - Returns an error if no company is found for the given criteria.

        Args:
            request (Request): The HTTP request object.
            company_id (uuid.UUID, optional): The ID of the company to retrieve.
            user_id (uuid.UUID, optional): The ID of the user whose companies are to be retrieved.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 200: Company details or list of companies successfully retrieved.
            - HTTP 404: Company or companies not found.
            - HTTP 500: Internal server error.
        """
        try:
            user = get_user_by_id(user_id=user_id)
            
            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            validate_role = validate_roles_for_company(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='read')
            
            if permission:
                return permission
            
            if company_id:
                company = Company.objects.filter(id=company_id).values().first()

                if not company:
                    return create_response(
                        success=False,
                        message='Company not found.',
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='Company details.',
                    data=company,
                    status=200
                )
            
            else:
                user_company = Company.objects.filter(user_id=user_id).values().all()

                if not user_company:
                    return create_response(
                        success=False,
                        message='Company not found.',
                        status=404
                    )
                
                return create_response(
                    success=True,
                    message='Company list.',
                    data=list(user_company),
                    status=200
                )

        except Exception as e:
            return create_response(
                success=False, 
                message='Something went wrong', 
                status=500
            )
        
    def post(self, request: Request, 
            user_id:uuid.UUID
        ) -> Response:
        """
        Handles POST requests to create a new company.

        This method:
        - Validates the incoming data using `CompanySerializer`.
        - Checks if the user exists using the `user_id`.
        - Ensures no duplicate company exists for the given user with the same data.
        - Creates a new company associated with the provided user.

        Args:
            request (Request): The HTTP request object containing company data.
            user_id (uuid.UUID): The ID of the user to associate the company with.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 201: Company successfully created.
            - HTTP 400: Validation errors.
            - HTTP 404: User not found or company already exists.
            - HTTP 500: Internal server error.
        """
        try:
            user = get_user_by_id(user_id=user_id)
            
            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            validate_role = validate_roles_for_company(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='write')
            
            if permission:
                return permission
            
            serializer = CompanySerializer(data=request.data)
            
            if serializer.is_valid():
                validated_data = serializer.validated_data

                if Company.objects.filter(user_id=user_id).first():
                    return create_response(
                        success=False,
                        message='Company already exist.',
                        status=404
                    )

                Company.objects.create(user_id=user, **validated_data)                

                return create_response(
                    success=True,
                    message='Company created',
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
            
        except Exception as e:
            return create_response(
                success=False, 
                message='Something went wrong', 
                status=500
            )
        
    
    def put(self, request: Request,
            company_id: uuid.UUID,
            user_id:uuid.UUID,
        ) -> Response:
        """
        Handles PUT requests to update an existing company.

        This method:
        - Checks if the company with the provided `company_id` exists.
        - Validates the incoming data using `CompanySerializer`.
        - Updates only the provided fields of the company using `partial=True`.
        - Saves the updated company data.

        Args:
            request (Request): The HTTP request object containing company data to update.
            company_id (uuid.UUID): The ID of the company to be updated.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 200: Company successfully updated.
            - HTTP 400: Validation errors.
            - HTTP 404: Company not found.
            - HTTP 500: Internal server error.
        """

        try:
            user = get_user_by_id(user_id=user_id)
            
            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            validate_role = validate_roles_for_company(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='update')
            
            if permission:
                return permission
            
            company = Company.objects.filter(id=company_id).first()
            
            if not company:
                return create_response(
                    success=False,
                    message='Company not found.',
                    status=404
                )
            
            serializer =  CompanySerializer(data=request.data, partial=True)
            
            if serializer.is_valid():
                form_data = serializer.validated_data

                company_update = update_record(company, form_data)

                if not company_update:
                    
                    return create_response(
                    success=False, 
                    message='Something went wrong', 
                    status=500
                )

                company.save()
                return create_response(
                    success=True,
                    message='Company Update.',
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
        
        except Exception as e:
            return create_response(
                success=False, 
                message='Something went wrong', 
                status=500
            )
        
    def delete(self, request: Request,
            company_id:uuid.UUID,
            user_id:uuid.UUID
        ) -> Response:
        """
        Handles DELETE requests to delete an existing company.

        This method:
        - Checks if the company with the provided `company_id` exists.
        - Deletes the company from the database.

        Args:
            request (Request): The HTTP request object.
            company_id (uuid.UUID): The ID of the company to be deleted.

        Returns:
            Response: A response with a status code and message indicating success or failure.
            - HTTP 204: Company successfully deleted.
            - HTTP 404: Company not found.
            - HTTP 500: Internal server error.
        """

        try:
            user = get_user_by_id(user_id=user_id)
            
            if not user:
                return create_response(
                    success=False,
                    message='User not found!',
                    status=404
                )
            
            validate_role = validate_roles_for_company(user=user)

            if validate_role:
                return validate_role
            
            permission = check_permissions(user=user, permission_type='read')
            
            if permission:
                return permission
            
            company = Company.objects.filter(id=company_id).first()
            
            if not company:
                return create_response(
                    success=False,
                    message='Company not found.',
                    status=404
                )
            
            company.delete()
            return create_response(
                success=True,
                message='Company delete.',
                status=204
            )
        
        except Exception as e:
            return create_response(
                success=False, 
                message='Something went wrong', 
                status=500
            )
        