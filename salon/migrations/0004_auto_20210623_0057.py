# Generated by Django 3.2.4 on 2021-06-23 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0003_auto_20210623_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsaloncategory',
            name='created',
        ),
        migrations.RemoveField(
            model_name='historicalsaloncategory',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='historicalsaloncategory',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='historicalsaloncategory',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='saloncategory',
            name='created',
        ),
        migrations.RemoveField(
            model_name='saloncategory',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='saloncategory',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='saloncategory',
            name='modified_by',
        ),
    ]
