# Generated by Django 4.2.5 on 2023-12-22 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyerregistration',
            old_name='user_emailid',
            new_name='user_email_id',
        ),
    ]
