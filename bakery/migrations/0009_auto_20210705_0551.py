# Generated by Django 3.2.4 on 2021-07-05 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0008_auto_20210705_0525'),
    ]

    operations = [
        migrations.AddField(
            model_name='damages',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='historicaldamages',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
