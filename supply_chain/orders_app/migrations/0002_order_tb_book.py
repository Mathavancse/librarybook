# Generated by Django 4.2.16 on 2024-11-12 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_tb',
            name='BOOK',
            field=models.TextField(default='default_value'),
        ),
    ]
