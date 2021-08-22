# Generated by Django 3.2.6 on 2021-08-13 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0017_project_status_pro'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name', '-name', 'company', 'price', 'start_date', 'end_date', 'status_pro']},
        ),
        migrations.AddField(
            model_name='interaction',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.company', verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='rating',
            field=models.CharField(choices=[('☆', '☆'), ('☆☆', '☆☆'), ('☆☆☆', '☆☆☆'), ('☆☆☆☆', '☆☆☆☆'), ('☆☆☆☆☆', '☆☆☆☆☆')], max_length=100, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status_pro',
            field=models.CharField(default='Еще не начат', max_length=100, verbose_name='Статус проекта'),
        ),
    ]
