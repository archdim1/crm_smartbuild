# Generated by Django 3.2.6 on 2021-08-15 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0026_auto_20210814_1856'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['title'], 'permissions': (('auth_user_view', 'Can view permission'),)},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['name'], 'permissions': (('auth_user_view', 'Can view permission'),)},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name', '-name', 'company', 'price', 'start_date', 'end_date', 'status_pro'], 'permissions': (('auth_user_view', 'Can view permission'),)},
        ),
    ]