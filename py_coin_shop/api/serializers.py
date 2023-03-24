import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from items.models import (
    Product,
    ProductImage,
    Order,
    ProductOrder,
    Wallet,
    MoneyTransfer,
)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp" + ext)

        return super().to_internal_value(data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "name",
            "description",
            "price",
            "amount",
        )
        model = Product


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "name",
            "price",
        )
        read_only_fields = (
            "name",
            "price",
        )
        model = Product


class ProductImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ("product", "image")
        model = ProductImage


class MoneyTransferSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        fields = (
            "amount",
            "description",
            "wallet_owner",
            "author",
            "created_at",
        )
        read_only_fields = ("author", "created_at")
        model = MoneyTransfer


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("user", "balance")
        read_only_fields = ("user", "balance")
        model = Wallet


class ProductOrderSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer()

    class Meta:
        fields = ("product", "amount")
        model = ProductOrder


class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(many=True, source="order_product.all")
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "products",
            "owner",
            "created_at",
        )
