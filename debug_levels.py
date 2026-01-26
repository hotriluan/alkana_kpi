import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alkana_kpi.settings')
django.setup()

from kpi_app.models import alk_employee
from django.contrib.auth.models import User

print("--- Checking Employees ---")
employees = alk_employee.objects.all()
for emp in employees:
    if emp.level == 2:
        print(f"User: {emp.user_id.username}, Name: {emp.name}, Level: {emp.level} [TARGET]")
    else:
        print(f"User: {emp.user_id.username}, Name: {emp.name}, Level: {emp.level}")
