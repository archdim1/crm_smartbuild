# Generated by Django 3.2.6 on 2021-08-19 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0040_auto_20210819_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='managercrm',
            name='full_name',
        ),
    ]