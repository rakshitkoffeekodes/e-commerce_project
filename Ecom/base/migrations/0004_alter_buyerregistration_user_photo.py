# Generated by Django 4.2.5 on 2023-12-22 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_buyerregistration_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyerregistration',
            name='user_photo',
            field=models.ImageField(default='default.jpg', null=True, upload_to='media'),
        ),
    ]
