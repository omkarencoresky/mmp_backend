from django.urls import path
from users.views.user_view import Register, Login


urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]