# Generated by Django 3.1.4 on 2021-04-27 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20210425_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='stu_check',
            field=models.BooleanField(default=False),
        ),
    ]
