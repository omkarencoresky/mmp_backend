from django.urls import path
from users.views.address_view import Addresses


urlpatterns = [
    path('user/<uuid:user_id>', Addresses.as_view()),
    path('user/<uuid:user_id>/address/<uuid:address_id>', Addresses.as_view()),

]