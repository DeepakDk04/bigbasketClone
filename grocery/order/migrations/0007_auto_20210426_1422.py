# Generated by Django 3.1.7 on 2021-04-26 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer',
            new_name='orderbycustomer',
        ),
    ]