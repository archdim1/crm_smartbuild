# Generated by Django 3.2.6 on 2021-08-10 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_alter_interaction_channel_of_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='reference_obj',
            field=models.CharField(choices=[('К заказчику', 'К заказчику'), ('От заказчика', 'От заказчика'), ('К компании', 'К компании'), ('От компании', 'От компании')], max_length=100, null=True, verbose_name='Вид связи'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='channel_of_reference',
            field=models.CharField(choices=[('Телефонный звонок', 'Телефонный звонок'), ('Письмо на E-mail', 'Письмо на E-mail'), ('Переписка в мессенджере', 'Переписка в мессенджере')], max_length=100, verbose_name='Канал связи'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='rating',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=100, verbose_name='Оценка'),
        ),
    ]
