# Generated by Django 4.2.5 on 2023-12-25 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_address_alter_buyerregistration_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('State Name', 'Andhra Pradesh'), ('State Name', 'Arunachal Pradesh'), ('State Name', 'Assam'), ('State Name', 'Bihar'), ('State Name', 'Chhattisgarh'), ('State Name', 'Goa'), ('State Name', 'Gujarat'), ('State Name', 'Haryana'), ('State Name', 'Himachal Pradesh'), ('State Name', 'Jharkhand'), ('State Name', 'Karnataka'), ('State Name', 'Kerala'), ('State Name', 'Madhya Pradesh'), ('State Name', 'Maharashtra'), ('State Name', 'Manipur'), ('State Name', 'Meghalaya'), ('State Name', 'Mizoram'), ('State Name', 'Nagaland'), ('State Name', 'Odisha'), ('State Name', 'Punjab'), ('State Name', 'Rajasthan'), ('State Name', 'Sikkim'), ('State Name', 'Tamil Nadu'), ('State Name', 'Telangana'), ('State Name', 'Tripura'), ('State Name', 'Uttar Pradesh'), ('State Name', 'Uttarakhand'), ('State Name', 'West Bengal'), ('State Name', 'Andaman and Nicobar Islands'), ('State Name', 'Chandigarh'), ('State Name', 'Dadra & Nagar Haveli and Daman & Diu'), ('State Name', 'Delhi'), ('State Name', 'Jammu and Kashmir'), ('State Name', 'Lakshadweep'), ('State Name', 'Puducherry'), ('State Name', 'Ladakh')], max_length=40),
        ),
    ]
