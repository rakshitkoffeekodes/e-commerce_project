# Generated by Django 4.2.5 on 2024-01-08 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0011_alter_buyercart_table_alter_buyerfeedback_table_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyerregistration',
            name='user_email_id',
        ),
        migrations.RemoveField(
            model_name='buyerregistration',
            name='user_firstname',
        ),
        migrations.RemoveField(
            model_name='buyerregistration',
            name='user_lastname',
        ),
        migrations.RemoveField(
            model_name='buyerregistration',
            name='user_password',
        ),
        migrations.AddField(
            model_name='buyerregistration',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
