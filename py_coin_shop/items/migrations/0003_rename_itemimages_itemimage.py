# Generated by Django 4.1.7 on 2023-03-16 19:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("items", "0002_alter_item_price_alter_itemorder_amount_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ItemImages",
            new_name="ItemImage",
        ),
    ]
