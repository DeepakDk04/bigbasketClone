# Generated by Django 3.1.7 on 2021-04-26 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_remove_customer_myorders'),
        ('order', '0005_remove_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
            preserve_default=False,
        ),
    ]
