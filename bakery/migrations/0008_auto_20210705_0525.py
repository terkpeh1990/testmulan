# Generated by Django 3.2.4 on 2021-07-05 05:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0007_historicalclosing_stocks_historicalcustomer_historicaldamages_historicalinventory_historicalinventor'),
    ]

    operations = [
        migrations.AddField(
            model_name='damages',
            name='cause',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicaldamages',
            name='cause',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
