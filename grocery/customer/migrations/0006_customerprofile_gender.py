# Generated by Django 3.1.7 on 2021-04-26 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20210423_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default='', max_length=6),
            preserve_default=False,
        ),
    ]