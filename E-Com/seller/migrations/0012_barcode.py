# Generated by Django 4.2.2 on 2023-12-25 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0011_rename_buyer_id_accept_buyer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
            ],
        ),
    ]
