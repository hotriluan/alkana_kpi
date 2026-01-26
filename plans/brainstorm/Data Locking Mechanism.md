Phase 1: Implementation Plan - Data Locking Mechanism
**Project:** Alkana KPI System
**Objective:** Implement a "Hard Lock" mechanism (`is_locked`) to prevent data modification by End Users (Level 2) after manager approval or period closure.
**Context:** The system has existing production data (6 months). Implementation must ensure data integrity for historical records.

---

## 1. Database Schema Modification
**Target File:** `kpi_app/models.py`
**Reference:** Data Model Documentation

### Objective
Add a boolean status field to the `Alk_KPI_Result` model to control editability.

### Implementation Steps
1.  Locate the `Alk_KPI_Result` class.
2.  Add the `is_locked` field.

### Code Snippet
```python
class Alk_KPI_Result(models.Model):
    # ... existing fields (year, semester, employee, achievement, etc.) ...

    # NEW FIELD
    is_locked = models.BooleanField(
        default=False, 
        verbose_name="Locked / Finalized",
        help_text="If checked, Level 2 employees cannot edit this result."
    )
Note: Setting default=False ensures that all existing 6 months of data will default to "Unlocked" status upon migration, preserving data integrity without data loss.

2. Admin Interface Logic Update
Target File: kpi_app/admin.py Reference: Admin Guide

Objective
Enforce "Read-Only" mode for Level 2 users when is_locked is True.

Provide a "Bulk Lock" action for Managers (Level 1) and Admins.

Implementation Steps
A. Define Bulk Actions
Add these functions outside or inside the Alk_KPI_ResultAdmin class.

Python

@admin.action(description='[LOCK] Finalize selected KPI Results')
def lock_kpi_results(modeladmin, request, queryset):
    # Permission check: Only Superuser or Level 0/1 can lock
    if not request.user.is_superuser:
        if hasattr(request.user, 'alk_employee') and request.user.alk_employee.level > 1:
            modeladmin.message_user(request, "Permission Denied: You cannot lock records.", level='ERROR')
            return
            
    updated_count = queryset.update(is_locked=True)
    modeladmin.message_user(request, f"Successfully locked {updated_count} records.")

@admin.action(description='[UNLOCK] Re-open selected KPI Results')
def unlock_kpi_results(modeladmin, request, queryset):
    # Strict permission check for unlocking
    if not request.user.is_superuser:
        if hasattr(request.user, 'alk_employee') and request.user.alk_employee.level > 1:
             modeladmin.message_user(request, "Permission Denied: You cannot unlock records.", level='ERROR')
             return

    updated_count = queryset.update(is_locked=False)
    modeladmin.message_user(request, f"Successfully unlocked {updated_count} records.")
B. Override get_readonly_fields
Modify the Alk_KPI_ResultAdmin class configuration.

Python

class Alk_KPI_ResultAdmin(admin.ModelAdmin):
    # ... existing configuration ...
    
    actions = [lock_kpi_results, unlock_kpi_results, ...] # Add new actions
    
    def get_readonly_fields(self, request, obj=None):
        # 1. Get default readonly fields defined in strict admin logic
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        # 2. Logic for Locked Records
        if obj and obj.is_locked:
            # Check user level
            user_level = 2 # Default to restricted
            if hasattr(request.user, 'alk_employee'):
                user_level = request.user.alk_employee.level
            
            # If User is Level 2 (Regular Employee) -> MAKE EVERYTHING READONLY
            if not request.user.is_superuser and user_level >= 2:
                return [f.name for f in self.model._meta.fields]
        
        return readonly_fields
3. Deployment & Safety Protocol
Reference: Security Configuration

Step 1: Backup (Mandatory)
Before applying changes, execute a full database dump to ensure safety of the 6-month historical data.

Bash

# Example for MySQL
mysqldump -u [user] -p[password] alkana_kpi > backup_pre_phase1.sql
Step 2: Apply Migrations
Run standard Django commands to update the database schema.

Bash

python manage.py makemigrations kpi_app
python manage.py migrate
Step 3: Verification
Log in as Superuser.

Check Alk KPI Results table.

Verify that existing records are intact and is_locked column exists (value is unchecked/False).

4. Post-Deployment Data Cleanup
Objective: Secure the historical "Gap" (Vùng trũng) for the past 6 months.

Action Required by Admin:

Login to Admin Panel -> Alk KPI Results.

Filter by Semester = "1st SEM" (and any previous periods).

Select All records.

Execute Action: "[LOCK] Finalize selected KPI Results".

Result: All historical data is now immutable for Level 2 users.

5. Verification Checklist (UAT)
[ ] Database: Field is_locked exists in alk_kpi_result table.

[ ] Logic: User Level 2 cannot edit a record where is_locked=True.

[ ] Logic: User Level 1 (Manager) CAN edit a record where is_locked=True (or unlock it).

[ ] Action: Bulk lock action works correctly on multiple rows.

[ ] Data: Old data (previous 6 months) remains correct and accessible.