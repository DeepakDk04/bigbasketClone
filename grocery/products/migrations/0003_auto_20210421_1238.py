# Generated by Django 3.1.7 on 2021-04-21 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210421_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.offer'),
        ),
    ]
