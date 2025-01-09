from django.urls import path
from travel_agency.views.transport_vehicle_view import TransportVehicleManagement


urlpatterns = [
    path('user/<uuid:user_id>', TransportVehicleManagement.as_view(), name='add_transport_vehicle'),
    path('user/<uuid:user_id>/vehicle/<uuid:transport_vehicle_id>', TransportVehicleManagement.as_view(), name='manage_transport_vehicle'),
]