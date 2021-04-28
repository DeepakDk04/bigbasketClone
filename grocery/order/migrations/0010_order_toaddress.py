# Generated by Django 3.1.7 on 2021-04-27 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_customer_myorders'),
        ('order', '0009_auto_20210426_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='toaddress',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='customer.deliveryaddress'),
            preserve_default=False,
        ),
    ]
