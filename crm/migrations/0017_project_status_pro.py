# Generated by Django 3.2.6 on 2021-08-12 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0016_alter_interaction_reference_obj'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status_pro',
            field=models.CharField(default='Еще не начат', max_length=100),
        ),
    ]