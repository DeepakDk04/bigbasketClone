# Generated by Django 3.1.7 on 2021-04-21 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('percentage', models.IntegerField()),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('expiry', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('isOffer', models.BooleanField(default=False)),
                ('stockCount', models.IntegerField()),
                ('category', models.ManyToManyField(to='products.Category')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.offer')),
            ],
        ),
    ]
