# Generated by Django 3.1.7 on 2021-04-21 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.offer'),
        ),
    ]