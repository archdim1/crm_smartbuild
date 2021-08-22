# Generated by Django 3.2.6 on 2021-08-13 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0024_alter_project_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='company',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.company', verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='customer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.customer', verbose_name='Заказчик проекта'),
        ),
    ]