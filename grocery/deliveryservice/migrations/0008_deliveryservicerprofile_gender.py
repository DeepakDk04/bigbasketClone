# Generated by Django 3.1.7 on 2021-04-26 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveryservice', '0007_deliveryservicer_mydeliveries'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryservicerprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default='Male', max_length=6),
            preserve_default=False,
        ),
    ]