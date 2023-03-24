from django.contrib import admin

from .models import (
    Product,
    ProductImage,
    Order,
    Wallet,
    MoneyTransfer,
    ProductOrder,
    models
)


@admin.register(Product)
class ItemAdmin(admin.ModelAdmin):
    """Класс конфигурации модели Item в админке"""
    list_display = (
        'pk',
        'name',
        'description',
        'price',
        'amount',
    )
    list_editable = ('price', 'amount')
    search_fields = ('name',)
    list_filter = ('price',)
    empty_value_display = '-пусто-'


@admin.register(ProductImage)
class ImagesAdmin(admin.ModelAdmin):
    """Класс конфигурации модели Images в админке"""
    list_display = (
        'pk',
        'product',
        'image',
    )
    list_editable = ('image',)
    search_fields = ('product',)
    empty_value_display = '-пусто-'


@admin.register(MoneyTransfer)
class MoneyTransferAdmin(admin.ModelAdmin):
    """Класс конфигурации модели MoneyTransfer в админке"""
    list_display = (
        'pk',
        'amount',
        'description',
        'wallet_owner',
        'author',
        'created_at',
    )
    list_editable = ('wallet_owner', 'amount')
    search_fields = ('wallet_owner',)
    empty_value_display = '-пусто-'


class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Класс конфигурации модели Order в админке"""
    inlines = (ProductOrderInline, )
    list_display = (
        'pk',
        'get_products',
        'owner',
        'created_at',
        'total_price',
    )
    search_fields = ('owner',)
    empty_value_display = '-пусто-'

    def get_products(self, obj):
        return "; ".join(
            [f"{product.name} цена: {product.price} "
             f"x {obj.order_product.get(order=obj, product=product).amount}"
             for product in obj.products.all()])


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Класс конфигурации модели Wallet в админке"""
    list_display = (
        'pk',
        'user',
        'balance',

    )
    search_fields = ('user',)
    empty_value_display = '-пусто-'
