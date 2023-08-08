from django.urls import path
from mywallet.views import initiate_wallet, wallet_actions, \
    wallet_transactions


urlpatterns = [
    path('init/', initiate_wallet),
    path('wallet/<str:operation>/', wallet_transactions),
    path('wallet/', wallet_actions),
]