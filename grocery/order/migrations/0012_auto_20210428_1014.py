# Generated by Django 3.1.7 on 2021-04-28 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_customer_myorders'),
        ('order', '0011_order_placedon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='toaddress',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.deliveryaddress'),
        ),
    ]
