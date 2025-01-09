from django.urls import path
from common_app.views.permission_view import PermissionManagement


urlpatterns = [
    path('user/<uuid:user_id>', PermissionManagement.as_view(), name='add_permission'),
    path('user/<uuid:user_id>/permission/<uuid:permission_id>', PermissionManagement.as_view(), name='manage_permission'),
]   