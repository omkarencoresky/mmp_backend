from django.urls import path
from users.views.company_view import CompanyManagement


urlpatterns = [
    path('get/<uuid:user_id>', CompanyManagement.as_view()),
    path('<uuid:company_id>', CompanyManagement.as_view()),
]   