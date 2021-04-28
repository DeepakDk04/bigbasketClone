# Generated by Django 3.1.7 on 2021-04-26 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deliveryservice', '0004_auto_20210425_1130'),
        ('customer', '0005_auto_20210423_2326'),
        ('order', '0002_auto_20210426_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.cart'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
        ),
        migrations.AlterField(
            model_name='order',
            name='deliveryservicer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deliveryservice.deliveryservicer'),
        ),
    ]