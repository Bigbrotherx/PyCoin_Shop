# Generated by Django 4.1.7 on 2023-03-16 13:31

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Укажите цену товара', max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))], verbose_name='Цена товара'),
        ),
        migrations.AlterField(
            model_name='itemorder',
            name='amount',
            field=models.PositiveSmallIntegerField(help_text='Укажите цену товара', verbose_name='Колличество единиц товара'),
        ),
        migrations.AlterField(
            model_name='moneytransfer',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='сумма'),
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Баланс пользователя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]