# Generated by Django 4.2.5 on 2024-01-03 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            ],
        ),
        migrations.CreateModel(
            name='BuyerFeedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback_description', models.TextField(max_length=500)),
                ('feedback_datetime', models.DateTimeField(auto_now_add=True)),
                ('feedback_rating', models.IntegerField()),
                ('feedback_photo', models.FileField(null=True, upload_to='buyer/')),
            ],
            options={
                'db_table': 'feedback_table',
            },
        ),
        migrations.CreateModel(
            name='BuyerPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='IND', max_length=3)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('order', models.CharField(max_length=100)),
                ('payment_intent_id', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BuyerRegistration',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_firstname', models.CharField(max_length=255)),
                ('user_lastname', models.CharField(max_length=255)),
                ('user_address', models.TextField(max_length=255)),
                ('user_photo', models.FileField(default='defult.jpg', null=True, upload_to='buyer/')),
                ('user_mobile_no', models.CharField(max_length=12, unique=True)),
                ('user_email_id', models.CharField(max_length=255, unique=True)),
                ('user_password', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('returns', models.CharField(max_length=100)),
                ('order_return_message', models.CharField(max_length=100, null='N/A')),
                ('return_shipping_Fee', models.IntegerField(default=0)),
                ('return_date', models.DateTimeField(null=True)),
                ('status', models.BooleanField(default=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.buyerregistration')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.buyerpayment')),
            ],
        ),
        migrations.CreateModel(
            name='Checkout_details',
            fields=[
                ('address', models.AutoField(default=None, primary_key=True, serialize=False)),
                ('street_address', models.CharField(max_length=100)),
                ('apartment_address', models.CharField(max_length=100)),
                ('pincode', models.IntegerField()),
                ('city', models.CharField(max_length=100)),
                ('select_state', models.CharField(choices=[('State Name', 'Andhra Pradesh'), ('State Name', 'Arunachal Pradesh'), ('State Name', 'Assam'), ('State Name', 'Bihar'), ('State Name', 'Chhattisgarh'), ('State Name', 'Goa'), ('State Name', 'Gujarat'), ('State Name', 'Haryana'), ('State Name', 'Himachal Pradesh'), ('State Name', 'Jharkhand'), ('State Name', 'Karnataka'), ('State Name', 'Kerala'), ('State Name', 'Madhya Pradesh'), ('State Name', 'Maharashtra'), ('State Name', 'Manipur'), ('State Name', 'Meghalaya'), ('State Name', 'Mizoram'), ('State Name', 'Nagaland'), ('State Name', 'Odisha'), ('State Name', 'Punjab'), ('State Name', 'Rajasthan'), ('State Name', 'Sikkim'), ('State Name', 'Tamil Nadu'), ('State Name', 'Telangana'), ('State Name', 'Tripura'), ('State Name', 'Uttar Pradesh'), ('State Name', 'Uttarakhand'), ('State Name', 'West Bengal'), ('State Name', 'Andaman and Nicobar Islands'), ('State Name', 'Chandigarh'), ('State Name', 'Dadra & Nagar Haveli and Daman & Diu'), ('State Name', 'Delhi'), ('State Name', 'Jammu and Kashmir'), ('State Name', 'Lakshadweep'), ('State Name', 'Pondicherry'), ('State Name', 'Ladakh')], max_length=40)),
                ('ord_rec_name', models.CharField(max_length=255)),
                ('ord_rec_mobile_no', models.CharField(max_length=12)),
                ('status', models.BooleanField(default=True)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.buyerregistration')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.buyercart')),
            ],
        ),
        migrations.CreateModel(
            name='BuyerPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(default=0)),
                ('qty', models.PositiveIntegerField(default=0)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.buyerregistration')),
                ('cart', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.buyercart')),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.checkout_details')),
            ],
        ),
    ]