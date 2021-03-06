# Generated by Django 3.1.7 on 2021-04-21 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doorno', models.CharField(max_length=10)),
                ('street', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=50)),
                ('landmark', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('contactno', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customer.deliveryaddress')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customer.customerprofile')),
            ],
        ),
    ]
