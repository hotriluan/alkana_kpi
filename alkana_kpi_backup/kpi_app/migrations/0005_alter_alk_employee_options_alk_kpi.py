# Generated by Django 5.2.1 on 2025-06-10 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_app', '0004_alter_alk_employee_options_alk_employee_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alk_employee',
            options={'ordering': ['dept', 'name', 'job_title']},
        ),
        migrations.CreateModel(
            name='alk_kpi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kpi_name', models.CharField(max_length=200)),
                ('kpi_type', models.CharField(choices=[('bigger_better', 'Bigger better result = achieve/target'), ('smaller_better', 'Smaller better result = target/achieve')], max_length=20)),
                ('from_sap', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('dept_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kpi_app.alk_dept_objective')),
                ('perspective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kpi_app.alk_perspective')),
            ],
        ),
    ]
