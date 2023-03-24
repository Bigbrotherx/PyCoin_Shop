from rest_framework import generics, viewsets, mixins
from django.shortcuts import get_object_or_404
from rest_framework import response

from .serializers import (
    MoneyTransferSerializer,
    MoneyTransfer,
    OrderSerializer,
    Order,
    ProductImageSerializer,
    ProductImage,
    ProductSerializer,
    Product,
    WalletSerializer,
    Wallet,
)


class WalletRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer

    def get_queryset(self):
        """Получение коментов для конкретного пользователя"""
        queryset = get_object_or_404(Wallet, user=self.kwargs.get("user_id"))
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        """Получение инстанса владельца для сохраннения в модели Order"""
        serializer.save(owner=self.request.user)


class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        """Получение картинок для конкретного товара"""
        queryset = get_object_or_404(
            ProductImage, item=self.kwargs.get("item_id")
        )
        return queryset


class MoneyTransferAPIView(generics.CreateAPIView, generics.ListAPIView):
    queryset = MoneyTransfer.objects.all()
    serializer_class = MoneyTransferSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
