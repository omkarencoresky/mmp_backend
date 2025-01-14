from django.urls import path
from common_app.views.user_permission_view import UserPermissionManagement


urlpatterns = [
    path('user/<uuid:granted_by>', UserPermissionManagement.as_view(), name='add_user_permission'),
    path('user/<uuid:granted_by>/permissions/<uuid:user_id>', UserPermissionManagement.as_view(), name='manage_permission'),
]   