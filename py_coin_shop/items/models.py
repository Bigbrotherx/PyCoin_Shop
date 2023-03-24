from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Product(models.Model):
    name = models.CharField("название товара", max_length=75, unique=True)
    description = models.TextField(
        "описание товара",
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        "Цена товара",
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.0"))],
        help_text="Укажите цену товара",
    )
    amount = models.PositiveSmallIntegerField(
        "колличество на складе", default=0
    )


def custom_image_path(instance, filename):
    """Функция создания уникального пути для изображений"""
    return f"items/images/{instance.product.id}/{filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to=custom_image_path)


class MoneyTransfer(models.Model):
    amount = models.DecimalField(
        "сумма",
        max_digits=20,
        decimal_places=2,
    )
    description = models.CharField(max_length=150)
    wallet_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="charges"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transfers"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    products = models.ManyToManyField(Product, through="ProductOrder")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    @property
    def total_price(self):
        return self.products.aggregate(
            total_price=models.Sum(
                models.F("product_order__amount") * models.F("price")
            )
        )["total_price"] or Decimal("0")

    def __str__(self) -> str:
        """Информация о заказе"""

        return f"{self.products}"


class ProductOrder(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product_order"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_product"
    )
    amount = models.PositiveSmallIntegerField(
        "Колличество единиц товара", help_text="Укажите цену товара"
    )

    def clean(self) -> None:
        if self.amount > self.product.amount:
            raise ValidationError("Нельзя заказать больше чем на складе!")


class Wallet(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.DecimalField(
        "Баланс пользователя",
        max_digits=20,
        decimal_places=2,
    )


@receiver(post_save, sender=Order)
@receiver(post_save, sender=MoneyTransfer)
def wallet_balance_callback(sender, instance, created, **kwargs):
    if isinstance(sender, Order):
        if created:
            order = instance
            order_total = order.total_price
            wallet = order.owner.wallet
            wallet.balance = models.F("balance") - order_total
            wallet.save(update_fields="balance")
    elif isinstance(sender, MoneyTransfer):
        if created:
            money_transfer = instance
            wallet = money_transfer.wallet_owner.wallet
            wallet.balance = models.F("balance") + money_transfer.amount
            wallet.save(update_fields="balance")
