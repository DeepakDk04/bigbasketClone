# Generated by Django 3.1.7 on 2021-04-26 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_customer_myorders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='myorders',
        ),
    ]