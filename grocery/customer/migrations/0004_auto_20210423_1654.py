# Generated by Django 3.1.7 on 2021-04-23 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20210423_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.ManyToManyField(blank=True, to='customer.DeliveryAddress'),
        ),
    ]
