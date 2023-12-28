# Generated by Django 4.2.2 on 2023-12-28 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0007_rename_product_items_product_product_sub_category'),
        ('base', '0007_payment_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('returns', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.buyerregistration')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.product')),
            ],
        ),
    ]
