# Generated by Django 3.1.4 on 2022-01-16 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partytree', '0003_products_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='customer',
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
