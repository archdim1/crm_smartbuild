# Generated by Django 3.2.6 on 2021-08-10 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20210810_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateTimeField(verbose_name='Дата окончания проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(verbose_name='Дата начала проекта'),
        ),
    ]
