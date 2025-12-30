# Permission Matrix - Alkana KPI System

This document details the access control system based on employee levels and user roles.

## Overview

The Alkana KPI system implements a **5-level permission hierarchy** (0-4) that controls:
- Which KPI results users can view
- Which fields users can edit
- Who can import/export data
- Access to admin functions

**Implementation**: [kpi_app/admin.py](../../kpi_app/admin.py#L244-L340)

## Permission Levels

### Level 0: Group Manager
**Highest employee level** (cross-department oversight)

**View Permissions**:
- All KPI results for employees in the same **department group**
- Spans multiple departments within the group

**Edit Permissions**:
- Can view KPI results (read-mostly)
- **Cannot edit** `kpi` or `max` fields
- Limited field editing on own records

**Scope Calculation**:
```python
# Get employee's department group
dept_group = employee.dept.group

# Get all departments in this group
depts_in_group = Alk_Dept.objects.filter(group=dept_group)

# Show KPI results from all employees in these departments
return results.filter(employee__dept__in=depts_in_group)
```

**Use Cases**:
- Group directors overseeing multiple related departments
- Cross-functional managers monitoring group performance
- Executive-level visibility across department groups

**Example**:
- Employee in "Finance - 410" group can see:
  - Finance Department employees
  - Accounting Department employees
  - Any other dept with group = "Finance - 410"

---

### Level 1: Department Manager
**Department-wide access**

**View Permissions**:
- All KPI results for employees in the **same department**
- Department-scoped visibility only

**Edit Permissions**:
- Can edit `kpi` field (change which KPI is assigned)
- Can edit `max` field (adjust maximum threshold)
- Can edit most other fields in KPI results

**Read-Only Fields** (even for Level 1):
- `employee` (always readonly)
- `final_result` (auto-calculated)
- `achivement` (if kpi.from_sap = True)
- `target_input` (if kpi.percentage_cal = False)

**Scope Calculation**:
```python
# Show KPI results from all employees in same department
return results.filter(employee__dept=employee.dept)
```

**Use Cases**:
- Department heads
- Department managers
- Team leads with department oversight

**Example**:
- Finance Manager can see/edit:
  - All Finance Department employees' KPI results
  - Can adjust KPI assignments and thresholds
  - Cannot see other departments

---

### Level 2: Regular Employee (Default)
**Self-only access with limited editing**

**View Permissions**:
- Only their own KPI results

**Edit Permissions**:
- Can edit data entry fields:
  - `achivement` (if not from_sap)
  - `target_input` (if percentage_cal = True)
  - `weigth`, `min`, `target_set` (depending on config)
- **Cannot edit**:
  - `employee` (always readonly)
  - `kpi` (readonly for level 2+)
  - `max` (readonly for level 2+)
  - `final_result` (auto-calculated)

**Scope Calculation**:
```python
# Show only their own KPI results
return results.filter(employee__user_id=user)
```

**Use Cases**:
- Most employees (default level)
- Individual contributors
- Staff members tracking their own KPIs

**Example**:
- Regular employee can:
  - View own KPI results only
  - Update achievement values
  - Cannot change KPI assignments or thresholds

---

### Level 3: Restricted Employee
**Same as Level 2 with potential future restrictions**

**Current Behavior**: Identical to Level 2

**View Permissions**:
- Only their own KPI results

**Edit Permissions**:
- Same as Level 2

**Scope Calculation**:
- Same as Level 2

**Use Cases**:
- Contract workers
- Temporary employees
- Employees with special restrictions

**Future Extension**:
- Could be configured for more restrictive access
- Could limit editing during certain periods
- Could require approval for changes

---

### Level 4: Read-Only Employee
**Same as Level 2/3 (currently no special restrictions)**

**Current Behavior**: Identical to Level 2 and 3

**Recommended Future Behavior**:
- Read-only access to own KPI results
- No editing permissions
- View-only interface

**Use Cases**:
- Auditors
- Observers
- Historical record viewing

---

### Superuser (Django Admin)
**Full system access** (not an employee level)

**View Permissions**:
- **All records** across all departments, groups, and employees
- No filtering restrictions

**Edit Permissions**:
- Can edit **all fields** except auto-calculated ones
- Can edit `kpi` and `target_set` (locked for others)
- Can still have readonly fields based on KPI config:
  - `achivement` (if kpi.from_sap = True)
  - `target_input` (if kpi.percentage_cal = False)
  - `final_result` (always auto-calculated)

**Special Permissions**:
- **Import/Export**: Only superusers can import
- **User Management**: Create/modify Django users
- **All Admin Functions**: Full Django admin access

**Use Cases**:
- System administrators
- IT support staff
- Database administrators

**Security Note**: Limit superuser accounts to trusted personnel only.

---

## Permission Matrix Table

| Feature / Field | Superuser | Level 0 (Group) | Level 1 (Dept) | Level 2 (Regular) | Level 3/4 |
|-----------------|-----------|-----------------|----------------|-------------------|-----------|
| **View Scope** | All | Dept Group | Department | Self Only | Self Only |
| **Edit: employee** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Edit: kpi** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Edit: max** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Edit: target_set** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Edit: weigth** | ✅ | Limited | Limited | Limited | Limited |
| **Edit: min** | ✅ | Limited | Limited | Limited | Limited |
| **Edit: target_input** | Conditional | Conditional | Conditional | Conditional | Conditional |
| **Edit: achivement** | Conditional | Conditional | Conditional | Conditional | Conditional |
| **Edit: final_result** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Import Data** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Export Data** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **User Management** | ✅ | ❌ | ❌ | ❌ | ❌ |

**Legend**:
- ✅ = Always allowed
- ❌ = Always forbidden
- **Limited** = Allowed but may be readonly based on configuration
- **Conditional** = Depends on KPI flags (from_sap, percentage_cal)

---

## Conditional Field Access

### target_input Field

**Readonly When**:
```python
kpi.percentage_cal == False
```

**Editable When**:
```python
kpi.percentage_cal == True
```

**Logic**:
- When percentage_cal = False, target_input is auto-set to target_set value
- User should not manually edit it
- When percentage_cal = True, user must enter actual target value

**Applies To**: All permission levels (including superuser)

---

### achivement Field

**Readonly When**:
```python
kpi.from_sap == True
```

**Editable When**:
```python
kpi.from_sap == False
```

**Logic**:
- When data comes from SAP integration, achievement is imported automatically
- Manual editing would be overwritten by next SAP sync
- When not from SAP, user must manually enter achievement

**Applies To**: All permission levels (including superuser)

---

### final_result Field

**Always Readonly**: ❌

**Logic**:
- Auto-calculated via `calculate_final_result()` method
- Recalculated on every save
- Cannot be manually edited by anyone

**Applies To**: All users without exception

---

## Permission Implementation

### View Permission Code

**Location**: [admin.py](../../kpi_app/admin.py#L244-L267) - `get_queryset()` method

```python
def get_queryset(self, request):
    qs = super().get_queryset(request)
    user = request.user
    
    # Superuser sees everything
    if user.is_superuser:
        return qs
    
    # Get employee record
    try:
        employee = alk_employee.objects.get(user_id=user)
    except alk_employee.DoesNotExist:
        return qs.none()  # No employee = no access
    
    # Level 1: Department scope
    if employee.level == 1:
        return qs.filter(employee__dept=employee.dept)
    
    # Level 0: Department group scope
    elif employee.level == 0:
        dept_group = employee.dept.group
        depts_in_group = alk_dept.objects.filter(group=dept_group)
        return qs.filter(employee__dept__in=depts_in_group)
    
    # Level 2, 3, 4: Self only
    else:
        return qs.filter(employee__user_id=user)
```

---

### Edit Permission Code

**Location**: [admin.py](../../kpi_app/admin.py#L275-L340) - `get_readonly_fields()` method

```python
def get_readonly_fields(self, request, obj=None):
    ro = list(self.readonly_fields)
    
    # Employee always readonly
    if 'employee' not in ro:
        ro.append('employee')
    
    user = request.user
    
    # Superuser special handling
    if user.is_superuser:
        # Can edit kpi and target_set
        if 'kpi' in ro:
            ro.remove('kpi')
        if 'target_set' in ro:
            ro.remove('target_set')
        
        # But from_sap still makes achievement readonly
        if obj and obj.kpi and obj.kpi.from_sap:
            if 'achivement' not in ro:
                ro.append('achivement')
        return ro
    
    # Get employee level
    try:
        employee = alk_employee.objects.get(user_id=user)
        
        # Level 1 can edit kpi and max
        if employee.level == 1:
            if 'kpi' in ro:
                ro.remove('kpi')
            if 'max' in ro:
                ro.remove('max')
        else:
            # Level 2+ cannot edit kpi or max
            if 'kpi' not in ro:
                ro.append('kpi')
            if 'max' not in ro:
                ro.append('max')
    
    except alk_employee.DoesNotExist:
        # No employee record = max restrictions
        if 'kpi' not in ro:
            ro.append('kpi')
    
    # from_sap logic applies to all
    if obj and obj.kpi and obj.kpi.from_sap:
        if 'achivement' not in ro:
            ro.append('achivement')
    
    # percentage_cal logic applies to all
    if obj and obj.kpi and obj.kpi.percentage_cal is False:
        if 'target_input' not in ro:
            ro.append('target_input')
    
    return ro
```

---

### Import Permission Code

**Location**: [admin.py](../../kpi_app/admin.py#L269-L273) - `has_import_permission()` method

```python
def has_import_permission(self, request):
    """Only superuser can import"""
    return request.user.is_superuser
```

---

## Permission Flow Examples

### Example 1: Level 1 Manager Editing KPI Result

**User**: John (Level 1, Finance Manager)

**Action**: Edit KPI Result for employee in Finance Dept

**View Permission Check**:
```python
# John's level = 1
# Filter: employee__dept = Finance
# Result: Can see all Finance dept employees' KPI results ✅
```

**Edit Permission Check**:
```python
# Readonly fields calculation:
ro = ['employee']  # Always readonly

# John is level 1, not superuser
# Remove 'kpi' and 'max' from readonly
ro = ['employee']  # kpi and max are editable ✅

# Check KPI configuration
if obj.kpi.from_sap == True:
    ro.append('achivement')  # Make achievement readonly

if obj.kpi.percentage_cal == False:
    ro.append('target_input')  # Make target_input readonly

# Final readonly fields: ['employee', 'achivement', 'target_input']
# Editable: kpi, max, weigth, min, target_set ✅
```

---

### Example 2: Regular Employee (Level 2) Updating Own Achievement

**User**: Sarah (Level 2, Accountant)

**Action**: Update own KPI result achievement

**View Permission Check**:
```python
# Sarah's level = 2
# Filter: employee__user_id = Sarah's user
# Result: Can only see own KPI results ✅
```

**Edit Permission Check**:
```python
# Readonly fields calculation:
ro = ['employee']

# Sarah is level 2 (not 0 or 1)
# Add 'kpi' and 'max' to readonly
ro = ['employee', 'kpi', 'max']  # Cannot edit kpi or max ❌

# Check KPI configuration
if obj.kpi.from_sap == False:
    # Achievement is editable ✅
    pass

if obj.kpi.percentage_cal == True:
    # target_input is editable ✅
    pass

# Final readonly fields: ['employee', 'kpi', 'max']
# Editable: weigth, min, target_set, target_input, achivement ✅
```

---

### Example 3: Superuser Editing SAP-Integrated KPI

**User**: Admin (Superuser)

**Action**: Edit KPI result with from_sap=True

**View Permission Check**:
```python
# Admin is superuser
# No filtering: Can see ALL records ✅
```

**Edit Permission Check**:
```python
# Readonly fields calculation:
ro = ['employee']

# Admin is superuser
# Can edit kpi and target_set ✅

# But check KPI configuration
if obj.kpi.from_sap == True:
    ro.append('achivement')  # Achievement readonly even for superuser ❌

# Final readonly fields: ['employee', 'achivement']
# Editable: kpi, max, target_set, weigth, min, target_input ✅
# (Almost everything except SAP-controlled achievement)
```

---

## Security Recommendations

### Account Management

1. **Limit Superusers**: Only create superuser accounts for trusted IT personnel
2. **Use Levels Appropriately**: Assign level 1 only to actual managers
3. **Regular Audits**: Review employee levels periodically
4. **Remove Old Accounts**: Deactivate accounts for terminated employees

### Password Policy

1. **Strong Passwords**: Enforce minimum 12 characters, mixed case, numbers, symbols
2. **Regular Changes**: Require password changes every 90 days
3. **No Sharing**: Each user must have unique credentials
4. **Two-Factor Authentication**: Consider enabling 2FA for sensitive accounts

### Data Access

1. **Principle of Least Privilege**: Grant minimum necessary access
2. **Monitor Changes**: Log all admin changes for audit trail
3. **Restrict Import**: Import permission reserved for superuser only
4. **Review Exports**: Monitor who exports large datasets

### Django Configuration

```python
# settings.py - Security settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Session security
SESSION_COOKIE_AGE = 3600  # 1 hour timeout
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # HTTPS only
```

---

## Extending Permissions

### Adding New Permission Levels

To add a new level (e.g., Level 5 for external auditors):

1. **Update get_queryset()**:
```python
elif employee.level == 5:
    # Read-only, department scope
    return qs.filter(employee__dept=employee.dept)
```

2. **Update get_readonly_fields()**:
```python
elif employee.level == 5:
    # All fields readonly except viewing
    return list(self.model._meta.fields)
```

3. **Document the new level** in this guide

### Field-Level Permissions

To add more granular field permissions:

```python
def get_readonly_fields(self, request, obj=None):
    ro = super().get_readonly_fields(request, obj)
    
    # Custom: Only superuser can edit weights
    if not request.user.is_superuser:
        if 'weigth' not in ro:
            ro.append('weigth')
    
    return ro
```

---

## Troubleshooting Permissions

### Issue: User can't see any records

**Check**:
1. Is user linked to an employee record?
2. What is employee's level?
3. Are there KPI results matching the scope?

**Debug**:
```python
python manage.py shell
from kpi_app.models import alk_employee
from django.contrib.auth.models import User

user = User.objects.get(username='username')
try:
    emp = alk_employee.objects.get(user_id=user)
    print(f"Level: {emp.level}, Dept: {emp.dept}, Group: {emp.dept.group}")
except:
    print("No employee record found!")
```

---

### Issue: Field unexpectedly readonly

**Check**:
1. User's employee level
2. KPI flags: from_sap, percentage_cal
3. Field name (employee, final_result always readonly)

**Debug**: Check `get_readonly_fields()` output in Django debug toolbar or logs

---

**Last Updated**: December 30, 2025

For admin operations, see [Admin Guide](admin-guide.md).
