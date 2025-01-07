from django.urls import path
from users.views.address_view import Addresses


urlpatterns = [
    path('address/get/<uuid:user_id>', Addresses.as_view()),
    path('address/<uuid:address_id>', Addresses.as_view()),

]