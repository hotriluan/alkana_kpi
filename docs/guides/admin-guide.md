# Admin Guide - Alkana KPI System

This guide covers the Django Admin interface operations for managing the Alkana KPI system.

## Table of Contents
- [Overview](#overview)
- [Accessing the Admin Interface](#accessing-the-admin-interface)
- [User Roles and Permissions](#user-roles-and-permissions)
- [Managing Reference Data](#managing-reference-data)
- [Managing Employees](#managing-employees)
- [Managing KPIs](#managing-kpis)
- [Managing KPI Results](#managing-kpi-results)
- [Import/Export Operations](#importexport-operations)
- [Reporting Features](#reporting-features)
- [Common Tasks](#common-tasks)

## Overview

The Django Admin interface is the primary tool for managing the Alkana KPI system. It provides:

- **CRUD Operations** for all models
- **Import/Export** functionality for bulk data management
- **Filtering and Search** to find records quickly
- **Permission-based Access Control** based on employee levels
- **Inline Editing** for related records
- **Custom Display Formatters** for percentages and calculations

**Access URL**: `http://yourdomain.com/admin` or `http://127.0.0.1:8000/admin` (development)

## Accessing the Admin Interface

### 1. Login

Navigate to the admin URL and log in with your credentials:
- **Username**: Your assigned username or email
- **Password**: Your password

### 2. Main Dashboard

After login, you'll see the admin dashboard with available sections:

**AUTHENTICATION AND AUTHORIZATION**
- Groups
- Users

**KPI_APP**
- Alk Depts
- Alk Dept Groups
- Alk Employees
- Alk Job Titles
- Alk KPIs
- Alk KPI Results
- Alk Objectives
- Alk Perspectives

## User Roles and Permissions

### Superuser (Django Admin)
- **Full Access**: Can view, edit, delete all records
- **Import/Export**: Can use import/export features
- **User Management**: Can create/modify users
- **No Restrictions**: All fields editable

### Employee Level 1 (Manager)
- **Department Scope**: Can view/edit KPI results for entire department
- **Field Editing**: Can edit `kpi` and `max` fields in KPI results
- **No Import**: Cannot use import functionality

### Employee Level 0 (Group Manager)
- **Group Scope**: Can view/edit KPI results for all departments in their group
- **Limited Editing**: Cannot edit `kpi` or `max` fields
- **Read-Mostly**: Primarily for monitoring across groups

### Employee Level 2+ (Regular/Restricted)
- **Self Only**: Can only view/edit their own KPI results
- **Restricted Fields**: Most fields are read-only
- **Limited Access**: Cannot modify KPI definitions or targets

### Permission Matrix

See [Permission Matrix](permission-matrix.md) for detailed access control rules.

## Managing Reference Data

### Departments (Alk_Dept)

**Purpose**: Define organizational departments

**Steps to Add**:
1. Navigate to **KPI_APP → Alk Depts**
2. Click **Add Alk Dept**
3. Fill in:
   - **Dept name**: Full department name (e.g., "Finance")
   - **Dept abbrev**: Short code (e.g., "FIN")
   - **Dept group**: Group classification (e.g., "Finance - 410")
4. Click **Save**

**List View Features**:
- Search by dept name or abbreviation
- Filter by dept group
- Sort by any column

---

### Department Groups (Alk_Dept_Group)

**Purpose**: Group departments for higher-level management

**Steps to Add**:
1. Navigate to **KPI_APP → Alk Dept Groups**
2. Click **Add Alk Dept Group**
3. Fill in:
   - **Dept group**: Unique group name (e.g., "Finance - 410")
   - **Dept group abbrev**: Optional abbreviation
4. Click **Save**

**Note**: Ensure dept_group value matches exactly with references in Alk_Dept

---

### Job Titles (Alk_Job_Title)

**Purpose**: Define job positions within departments

**Steps to Add**:
1. Navigate to **KPI_APP → Alk Job Titles**
2. Click **Add Alk Job Title**
3. Fill in:
   - **Job title**: Position name (e.g., "Finance Manager")
   - **Job title abbrev**: Optional abbreviation
   - **Dept**: Select department from dropdown
4. Click **Save**

---

### Perspectives (Alk_Perspective)

**Purpose**: Categorize KPIs by business perspective (Balanced Scorecard)

**Common Perspectives**:
- Financial
- Customer
- Internal Process
- Learning & Growth

**Steps to Add**:
1. Navigate to **KPI_APP → Alk Perspectives**
2. Click **Add Alk Perspective**
3. Fill in perspective name and abbreviation
4. Click **Save**

---

### Objectives (Alk_Objective)

**Purpose**: Define strategic objectives linked to KPIs

**Steps to Add**:
1. Navigate to **KPI_APP → Alk Objectives**
2. Click **Add Alk Objective**
3. Fill in objective name and abbreviation
4. Click **Save**

## Managing Employees

### Adding an Employee

**Prerequisites**: Create Django User account first

**Steps**:
1. **Create User** (if not exists):
   - Navigate to **AUTHENTICATION → Users**
   - Click **Add User**
   - Enter username and password
   - Click **Save and continue editing**
   - Fill in first name, last name, email
   - Set **Staff status** if admin access needed
   - Click **Save**

2. **Create Employee**:
   - Navigate to **KPI_APP → Alk Employees**
   - Click **Add Alk Employee**
   - Fill in:
     - **Emp code**: Unique employee code (e.g., "EMP001")
     - **User**: Select the Django user from dropdown
     - **Dept**: Select department
     - **Dept group**: Select department group
     - **Job title**: Select job title
     - **Level**: Set permission level (0-4)
   - **Name** will auto-populate from User's first/last name
   - Click **Save**

### Editing Employee Information

1. Navigate to **KPI_APP → Alk Employees**
2. Find employee (use search or filters)
3. Click on employee name
4. Edit fields as needed
5. Click **Save**

**Note**: If you change User's first/last name, update the employee record to sync the `name` field.

### Setting Employee Levels

| Level | Role | Recommended For |
|-------|------|-----------------|
| 0 | Group Manager | Group directors, cross-department managers |
| 1 | Department Manager | Department heads, managers |
| 2 | Regular Employee | Most staff (default) |
| 3 | Restricted Employee | Contract workers, limited access |
| 4 | Read-Only | View-only access |

## Managing KPIs

### Creating a KPI

**Steps**:
1. Navigate to **KPI_APP → Alk KPIs**
2. Click **Add Alk KPI**
3. Fill in:
   - **Kpi name**: Descriptive KPI name (e.g., "Revenue Growth Q1")
   - **Dept obj**: Select department objective
   - **Perspective**: Select perspective
   - **Kpi type**: Choose calculation type:
     - **1 - Bigger better**: Higher achievement is better (revenue, sales)
     - **2 - Smaller better**: Lower achievement is better (costs, cycle time)
     - **3 - Mistake**: Mistake counting (defects, incidents)
   - **From sap**: Check if data comes from SAP system
   - **Active**: Keep checked to use this KPI
   - **Percentage cal**: Check if using percentage calculation mode
   - **Get 1 is zero**: Check for zero-tolerance KPIs (any occurrence = 0 score)
   - **Percent display**: Check to display result as percentage in UI
4. Click **Save**

### KPI Configuration Examples

**Example 1: Revenue Growth (Percentage Mode)**
```
KPI Name: Quarterly Revenue Growth
Kpi Type: 1 - Bigger better
Percentage Cal: ✓ (checked)
From SAP: ✓ (if integrated)
Active: ✓
```

**Example 2: Cost Reduction (Direct Mode)**
```
KPI Name: Operating Cost Reduction
Kpi Type: 2 - Smaller better
Percentage Cal: ☐ (unchecked)
Active: ✓
```

**Example 3: Safety Incidents (Zero Tolerance)**
```
KPI Name: Safety Violations
Kpi Type: 1 (doesn't matter with get_1_is_zero)
Get 1 is zero: ✓ (checked)
Active: ✓
```

### Editing KPIs

**Permission Requirements**:
- Superuser: Can edit all fields
- Level 1 (Manager): Can edit kpi field in KPI Results
- Others: Read-only

**Steps**:
1. Navigate to **KPI_APP → Alk KPIs**
2. Click on KPI name
3. Edit fields (if permitted)
4. Click **Save**

## Managing KPI Results

### Adding KPI Result

**Steps**:
1. Navigate to **KPI_APP → Alk KPI Results**
2. Click **Add Alk KPI Result**
3. Fill in:
   - **Year**: Year (e.g., 2025)
   - **Semester**: Select "1st SEM" or "2nd SEM"
   - **Month**: Select period ("1st" through "5th" or "final")
   - **Employee**: Select employee from dropdown
   - **Kpi**: Select KPI definition
   - **Weigth**: Enter weight (e.g., 0.25 for 25%)
   - **Min**: Minimum threshold (default 0.4)
   - **Max**: Maximum threshold (default 1.4)
   - **Target set**: Target ratio/percentage
   - **Target input**: Actual target value (auto-set if percentage_cal=False)
   - **Achivement**: Actual achievement value
   - **Active**: Keep checked
4. Click **Save**

**Result**: `final_result` is automatically calculated and saved.

### Field Behavior by KPI Configuration

**If `kpi.percentage_cal = False`**:
- `target_input` field is **read-only** (auto-set to `target_set`)
- Direct ratio calculation used

**If `kpi.from_sap = True`**:
- `achivement` field is **read-only** (data from SAP)
- Must update via import or API integration

**If `kpi.get_1_is_zero = True`**:
- Any `achivement > 0` → `final_result = 0`
- `achivement = 0` → `final_result = weight * max`

### Bulk Editing

**Using Admin Actions**:
1. Navigate to **KPI_APP → Alk KPI Results**
2. Filter/search for records
3. Select checkboxes for records to edit
4. Choose action from dropdown:
   - **Delete selected**: Delete records (careful!)
   - **Export selected** (if available)
5. Click **Go**

### Viewing Results

**List View Columns**:
- Year, Semester, Month
- Employee name
- KPI name
- Weight (%), Target Set, Min, Max
- Target Input, Achievement
- **Final Result (%)**: Calculated score displayed as percentage
- Active status

**Filtering Options**:
- By year, semester, month
- By employee
- By KPI
- By active status

**Search**: Search by employee name or KPI name

## Import/Export Operations

### Export to Excel

**Permission**: All users can export (limited by their view permissions)

**Steps**:
1. Navigate to the model (e.g., **Alk KPI Results**)
2. Apply filters to narrow down records (optional)
3. Click **Export** button (top right)
4. Select format: **xlsx** (Excel)
5. Click **Submit**
6. File downloads automatically

**Exported Columns**: All visible fields plus additional calculated fields

---

### Import from Excel

**Permission**: **Superuser only**

**Steps**:
1. **Prepare Excel File**:
   - Use exported file as template
   - Ensure column names match exactly
   - Fill in required fields
   - Remove ID column for new records

2. **Import**:
   - Navigate to the model (e.g., **Alk KPI Results**)
   - Click **Import** button
   - Click **Choose File** and select Excel file
   - Review data preview
   - Click **Confirm import**

3. **Validation**:
   - System validates all fields
   - Shows errors if any (fix and retry)
   - Displays success message with count

**Import File Format**:
See [Import/Export Guide](import-export-guide.md) for detailed specifications.

**Common Import Errors**:
- **Invalid foreign key**: Referenced employee/KPI doesn't exist
- **Missing required field**: Ensure all required columns filled
- **Duplicate emp_code**: Employee codes must be unique
- **Invalid choice**: Check semester/month values match choices

## Reporting Features

### KPI Report View

**Access**: Navigate to main KPI URL (not admin)

**Features**:
- Filter by semester, month, department
- Paginated results (100 per page)
- Export filtered results to Excel
- View total scores

**URL**: `/kpi/report/` (configure in urls.py)

### Using Django Admin Filters

**Available Filters**:
- Department
- Department Group
- Employee Level
- Year, Semester, Month
- Active status
- KPI Type

**Steps**:
1. Navigate to list view
2. Use filter sidebar on right
3. Click filter options to apply
4. Combine multiple filters

### Custom Queries

For complex reports, use Django shell:

```python
python manage.py shell
```

```python
from kpi_app.models import Alk_KPI_Result
from django.db.models import Sum

# Total score for employee in semester
results = Alk_KPI_Result.objects.filter(
    employee__emp_code='EMP001',
    year=2025,
    semester='1st SEM',
    month='final'
)
total_score = results.aggregate(Sum('final_result'))
print(total_score)
```

## Common Tasks

### Task 1: Set Up New Employee with KPIs

1. Create Django User
2. Create Employee record
3. Assign KPIs to employee:
   - Create KPI Result records for current semester
   - Set appropriate weights (should sum to 1.0)
   - Set min/max thresholds
   - Leave achievement blank initially

### Task 2: Update Monthly Achievements

1. Navigate to **Alk KPI Results**
2. Filter by:
   - Semester: "1st SEM"
   - Month: "1st"
   - Employee or Department
3. Click each record
4. Update **achivement** field
5. Save (final_result auto-calculates)

### Task 3: Close Semester and Calculate Final Scores

1. Ensure all monthly achievements entered
2. Create "final" month records if not exist
3. Set final achievements
4. Export results to Excel
5. Review total scores per employee

### Task 4: Set Up New Semester

1. Create new KPI Result records for new semester
2. Copy weights and thresholds from previous semester
3. Update target_set and target_input as needed
4. Leave achievements blank for future entry

### Task 5: Deactivate Old KPIs

1. Navigate to **Alk KPIs**
2. Find old/deprecated KPIs
3. Uncheck **Active** checkbox
4. Save

**Note**: Existing KPI Results remain intact, but KPI won't appear in new result creation.

### Task 6: Bulk Update Targets

1. Export current KPI Results to Excel
2. Update target_set/target_input columns in Excel
3. Import file back
4. System updates and recalculates final_result

## Tips and Best Practices

### Data Entry
- **Use Templates**: Export a record, duplicate rows in Excel, import back
- **Check Calculations**: Verify final_result makes sense after entry
- **Save Frequently**: Don't lose work on long forms

### Performance
- **Use Filters**: Don't load all records at once
- **Pagination**: Navigate through pages instead of showing all
- **Search**: Use search box for quick finding

### Data Integrity
- **Backup Before Import**: Export current data before bulk imports
- **Test on Staging**: Test imports on test environment first
- **Verify Totals**: Ensure weights sum to 1.0 per employee/semester

### Security
- **Change Password Regularly**: Update your password periodically
- **Log Out**: Always log out when done
- **Don't Share Credentials**: Each user should have unique account

## Troubleshooting

### Issue: Can't see any KPI results

**Cause**: Permission restrictions based on employee level

**Solution**: 
- Check your employee level
- Level 2+ can only see their own results
- Contact admin if you need broader access

---

### Issue: Target_input field is readonly

**Cause**: KPI has `percentage_cal = False`

**Solution**: This is expected behavior. Field auto-sets to target_set.

---

### Issue: Achievement field is readonly

**Cause**: KPI has `from_sap = True`

**Solution**: Data must come from SAP import. Contact IT for SAP integration.

---

### Issue: Final_result is 0 despite good achievement

**Possible Causes**:
1. Achievement below minimum threshold (check min value)
2. KPI has `get_1_is_zero = True` and achievement > 0
3. Null/missing target_input or achievement
4. Division by zero error

**Solution**: Review calculation logic in [KPI Calculation Logic](kpi-calculation-logic.md)

---

### Issue: Import fails with errors

**Common Fixes**:
- Ensure foreign key references exist (employee codes, KPI IDs)
- Check required fields are filled
- Verify semester/month values match exact choices ("1st SEM", not "1")
- Remove ID column for new records

---

For more issues, see [Troubleshooting Guide](troubleshooting.md).

---

**Last Updated**: December 30, 2025
