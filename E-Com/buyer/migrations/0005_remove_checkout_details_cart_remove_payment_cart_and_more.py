# Generated by Django 4.2.5 on 2024-01-01 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0004_buyercart_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout_details',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='cart',
        ),
        migrations.DeleteModel(
            name='BuyerCart',
        ),
    ]