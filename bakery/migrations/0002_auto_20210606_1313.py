# Generated by Django 3.1.4 on 2021-06-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='closing_stocks',
            name='close_status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='damages',
            name='dastatus',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='inventory_records',
            name='approval',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')], max_length=10, null=True),
        ),
    ]
