# Generated by Django 3.2.6 on 2021-08-18 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0037_auto_20210818_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='managercrm',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='managercrm',
            name='first_name_manager',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='managercrm',
            name='last_name_manager',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]