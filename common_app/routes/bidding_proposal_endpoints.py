from django.urls import path
from common_app.views.bidding_proposal_view import PackageProposalManagement


urlpatterns = [
    path('<uuid:user_id>', PackageProposalManagement.as_view(), name='add_bidding'),
    path('user/<uuid:user_id>/bid/<uuid:bid_id>', PackageProposalManagement.as_view(), name='manage_bidding'),
]       