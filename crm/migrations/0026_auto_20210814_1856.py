# Generated by Django 3.2.6 on 2021-08-14 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0025_auto_20210813_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(blank=True, choices=[('мужчина', 'мужчина'), ('женщина', 'женщина')], help_text='―――――', max_length=100, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(help_text='―ФИО', max_length=100, null=True, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(help_text='―――――', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='channel_of_reference',
            field=models.CharField(choices=[('Телефонный звонок', 'Телефонный звонок'), ('Переписка по E-mail', 'Переписка по E-mail'), ('Переписка в мессенджере', 'Переписка в мессенджере')], help_text='―――――', max_length=100, verbose_name='Канал связи'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='company',
            field=models.ForeignKey(blank=True, default=None, help_text='―――――', null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.company', verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='customer',
            field=models.ForeignKey(blank=True, default=None, help_text='―――――', null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.customer', verbose_name='Заказчик проекта'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='rating',
            field=models.CharField(choices=[('☆', '☆'), ('☆☆', '☆☆'), ('☆☆☆', '☆☆☆'), ('☆☆☆☆', '☆☆☆☆'), ('☆☆☆☆☆', '☆☆☆☆☆')], help_text='―――――', max_length=100, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='reference_obj',
            field=models.CharField(choices=[('с компанией', 'с компанией'), ('с заказчиком', 'с заказчиком')], help_text='―――――', max_length=100, null=True, verbose_name='Вид связи'),
        ),
        migrations.AlterField(
            model_name='project',
            name='customer',
            field=models.ForeignKey(help_text='―――――', null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.customer', verbose_name='Заказчик проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='price',
            field=models.IntegerField(help_text='― в долларах США', verbose_name='Стоимость проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status_pro',
            field=models.CharField(default='Еще не начат', help_text='―――――', max_length=100, verbose_name='Статус проекта'),
        ),
        migrations.CreateModel(
            name='ManagerCRM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='―ФИО', max_length=100, null=True, verbose_name='ФИО')),
                ('gender', models.CharField(blank=True, choices=[('мужчина', 'мужчина'), ('женщина', 'женщина')], help_text='―――――', max_length=100, verbose_name='Пол')),
                ('user', models.ForeignKey(help_text='―――――', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Имя пользователя')),
            ],
        ),
    ]