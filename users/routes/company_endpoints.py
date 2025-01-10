from django.urls import path
from users.views.company_view import CompanyManagement


urlpatterns = [
    path('user/<uuid:user_id>', CompanyManagement.as_view()),
    path('user/<uuid:user_id>/company/<uuid:company_id>', CompanyManagement.as_view()),
]   