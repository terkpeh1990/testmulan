# Generated by Django 3.1.4 on 2022-01-16 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partytree', '0004_auto_20220116_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_detailss',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partytree.products'),
        ),
    ]
