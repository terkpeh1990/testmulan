# Generated by Django 3.2.4 on 2021-09-20 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0013_auto_20210920_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder',
            name='clear',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='clear',
            field=models.BooleanField(default=False),
        ),
    ]
