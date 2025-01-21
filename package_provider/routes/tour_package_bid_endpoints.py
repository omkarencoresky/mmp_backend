from django.urls import path
from package_provider.views.tour_package_bid import TourPackageBidManagement, TourPackageAccept


urlpatterns = [
    path('user/<uuid:user_id>', TourPackageBidManagement.as_view(), name='add_tour_package'),
    path('user/<uuid:user_id>/accept/<uuid:package_bid_id>', TourPackageAccept.as_view(), name='add_tour_package'),
    path('user/<uuid:user_id>/package_bid/<uuid:package_bid_id>', TourPackageBidManagement.as_view(), name='manage_tour_package'),
]