# Generated by Django 3.2.4 on 2021-09-15 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0011_auto_20210904_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalloginrecords',
            name='is_hr',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='loginrecords',
            name='is_hr',
            field=models.BooleanField(default=False),
        ),
    ]
