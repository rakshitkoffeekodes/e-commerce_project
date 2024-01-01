# Generated by Django 4.2.5 on 2024-01-01 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
        ('buyer', '0005_remove_checkout_details_cart_remove_payment_cart_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('total', models.IntegerField(default=0)),
                ('product_color', models.CharField(max_length=50, null=True)),
                ('product_size', models.CharField(max_length=50, null=True)),
                ('status', models.BooleanField(default=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyer.buyerregistration')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.product')),
            ],
        ),
        migrations.AddField(
            model_name='checkout_details',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buyer.buyercart'),
        ),
        migrations.AddField(
            model_name='payment',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buyer.buyercart'),
        ),
    ]
