# Generated by Django 3.2.6 on 2021-08-12 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0015_auto_20210811_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='reference_obj',
            field=models.CharField(choices=[('к заказчику', 'к заказчику'), ('от заказчика', 'от заказчика'), ('к компании', 'к компании'), ('от компании', 'от компании')], max_length=100, null=True, verbose_name='Вид связи'),
        ),
    ]
