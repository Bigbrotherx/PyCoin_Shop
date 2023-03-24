from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import (
    ProductViewSet,
    ProductImageViewSet,
    OrderViewSet,
    MoneyTransferAPIView,
    WalletRetrieveAPIView,
)

router_v1 = DefaultRouter()
router_v1.register(r'items', ProductViewSet)
router_v1.register(r'order', OrderViewSet)
router_v1.register(
    r'items/(?P<item_id>)/images',
    ProductImageViewSet,
    basename='images')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/charge/', MoneyTransferAPIView.as_view()),
    path('v1/balance/<int:user_id>/', WalletRetrieveAPIView.as_view()),
    path('v1/get-token/', views.obtain_auth_token),
]
