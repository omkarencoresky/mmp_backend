from django.urls import path
from package_provider.views.tour_package_view import TourPackageManagement


urlpatterns = [
    path('user/<uuid:user_id>', TourPackageManagement.as_view(), name='add_tour_package'),
    path('user/<uuid:user_id>/package/<uuid:package_id>', TourPackageManagement.as_view(), name='manage_tour_package'),
]