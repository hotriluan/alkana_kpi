# Generated by Django 5.2.1 on 2025-06-18 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_app', '0021_alter_alk_kpi_result_achivement_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alk_kpi_result',
            name='min',
            field=models.DecimalField(decimal_places=3, default=0.4, max_digits=20),
        ),
    ]
