# Import/Export Guide - Alkana KPI System

This guide explains how to use the Excel import/export functionality for bulk data operations.

## Table of Contents
- [Overview](#overview)
- [Export Operations](#export-operations)
- [Import Operations](#import-operations)
- [File Format Specifications](#file-format-specifications)
- [Common Scenarios](#common-scenarios)
- [Troubleshooting](#troubleshooting)

## Overview

The system uses **django-import-export** with **openpyxl** to provide Excel (.xlsx) import/export capabilities for:

- **Alk_Employee**: Bulk employee management
- **Alk_KPI**: KPI definition management
- **Alk_KPI_Result**: Bulk KPI result entry and updates

**Supported Formats**: XLSX (Excel 2007+), XLS (Excel 97-2003), CSV

**Recommended**: Use XLSX format for best compatibility and features.

## Export Operations

### Who Can Export

**All users** can export data (limited by their view permissions):
- Superuser: Exports all records
- Level 0: Exports dept group scope
- Level 1: Exports department scope
- Level 2+: Exports own records only

### How to Export

1. Navigate to desired model (e.g., **KPI_APP → Alk KPI Results**)
2. **Apply filters** if you want to export a subset:
   - Filter by year, semester, month
   - Filter by department or employee
   - Use search to narrow results
3. Click **Export** button (top-right corner)
4. Select format: **xlsx** (recommended)
5. Click **Submit**
6. File downloads automatically

### Export File Structure

**Filename**: `<ModelName>-<Timestamp>.xlsx`

Example: `Alk_KPI_Result-2025-12-30.xlsx`

**Sheet Structure**:
- First row: Column headers
- Subsequent rows: Data records
- Includes all visible fields plus additional calculated fields

### Exported Fields

#### Alk_Employee Export

| Column | Description | Example |
|--------|-------------|---------|
| id | Record ID | 1 |
| emp_code | Employee code | EMP001 |
| user | Username | john.doe |
| dept | Department name | Finance |
| dept_group | Dept group name | Finance - 410 |
| job_title | Job title name | Finance Manager |
| level | Permission level | 1 |
| name | Full name | John Doe |

#### Alk_KPI Export

| Column | Description | Example |
|--------|-------------|---------|
| id | Record ID | 1 |
| kpi_name | KPI name | Revenue Growth |
| dept_obj | Objective name | Increase Revenue |
| perspective | Perspective name | Financial |
| kpi_type | Type (1, 2, or 3) | 1 |
| from_sap | Boolean | TRUE |
| active | Boolean | TRUE |
| percentage_cal | Boolean | FALSE |
| get_1_is_zero | Boolean | FALSE |
| percent_display | Boolean | TRUE |

#### Alk_KPI_Result Export

| Column | Description | Example |
|--------|-------------|---------|
| id | Record ID | 1 |
| year | Year | 2025 |
| semester | Semester | 1st SEM |
| month | Month | 1st |
| employee | Employee code | EMP001 |
| kpi | KPI name | Revenue Growth |
| weigth | Weight | 0.250 |
| min | Min threshold | 0.400 |
| max | Max threshold | 1.400 |
| target_set | Target ratio | 1.0000 |
| target_input | Target value | 1000000.0000 |
| achivement | Achievement | 1200000.0000 |
| final_result | Calculated score | 0.300 |
| active | Boolean | TRUE |

---

## Import Operations

### Who Can Import

**Superuser only** - Import functionality is restricted to prevent data integrity issues.

### Preparation Steps

1. **Export current data** as a template
2. **Backup your data** before importing
3. **Prepare Excel file** following format specifications
4. **Validate data** manually before import

### How to Import

1. Navigate to desired model (e.g., **KPI_APP → Alk KPI Results**)
2. Click **Import** button (top-right corner)
3. Click **Choose File** and select your Excel file
4. Click **Submit**
5. **Review the preview**:
   - Shows which records will be created/updated
   - Displays any validation errors
   - Check counts: New, Updated, Skipped
6. If OK, click **Confirm import**
7. If errors, click **Cancel** and fix the file

### Import Modes

**Create New Records**: Leave `id` column empty or remove it

**Update Existing Records**: Include `id` column with existing record IDs

**Mixed Mode**: Some rows with ID (update), some without (create)

---

## File Format Specifications

### General Rules

1. **First Row Must Be Headers**: Column names matching exported format
2. **Headers Are Case-Sensitive**: Use exact names from export
3. **Date Formats**: Use YYYY-MM-DD or system date format
4. **Decimal Separator**: Use period (.) not comma (,)
5. **Boolean Values**: TRUE/FALSE or 1/0
6. **Encoding**: UTF-8 (handles international characters)

### Required vs Optional Fields

#### Alk_Employee Import

**Required**:
- `emp_code` (unique)
- `user` (username, must exist in Django User table)
- `dept` (department name, must exist)
- `dept_group` (dept group name, must exist)
- `job_title` (job title name, must exist)

**Optional**:
- `id` (for updates)
- `level` (defaults to 2 if omitted)
- `name` (auto-generated from user if omitted)

**Example Row**:
```
emp_code: EMP002
user: jane.smith
dept: Finance
dept_group: Finance - 410
job_title: Accountant
level: 2
```

#### Alk_KPI Import

**Required**:
- `kpi_name`
- `dept_obj` (objective name, must exist)
- `perspective` (perspective name, must exist)
- `kpi_type` (1, 2, or 3)

**Optional**:
- `id` (for updates)
- `from_sap` (defaults to FALSE)
- `active` (defaults to TRUE)
- `percentage_cal` (defaults to FALSE)
- `get_1_is_zero` (defaults to FALSE)
- `percent_display` (defaults to FALSE)

**Example Row**:
```
kpi_name: Cost Reduction Initiative
dept_obj: Reduce Costs
perspective: Financial
kpi_type: 2
from_sap: FALSE
active: TRUE
percentage_cal: FALSE
```

#### Alk_KPI_Result Import

**Required**:
- `year`
- `semester` (exactly "1st SEM" or "2nd SEM")
- `month` (exactly "1st", "2nd", "3rd", "4th", "5th", or "final")
- `employee` (employee code, must exist)
- `kpi` (KPI name, must exist)
- `weigth`
- `target_set`

**Optional**:
- `id` (for updates)
- `min` (defaults to 0.4)
- `max` (defaults to 1.4)
- `target_input` (auto-set if percentage_cal=False)
- `achivement` (can be blank for future entry)
- `active` (defaults to TRUE)
- `final_result` (auto-calculated, ignored on import)

**Example Row**:
```
year: 2025
semester: 1st SEM
month: 1st
employee: EMP001
kpi: Revenue Growth
weigth: 0.250
min: 0.400
max: 1.400
target_set: 1.0000
target_input: 1000000.0000
achivement: 1200000.0000
active: TRUE
```

---

### Foreign Key References

**Important**: Foreign keys must reference existing records using the display value (not ID).

| Field | Reference Type | Must Match |
|-------|---------------|------------|
| employee | Employee code | Alk_Employee.emp_code |
| kpi | KPI name | Alk_KPI.kpi_name |
| user | Username | User.username |
| dept | Dept name | Alk_Dept.dept_name |
| dept_group | Group name | Alk_Dept_Group.dept_group |
| job_title | Title name | Alk_Job_Title.job_title |
| dept_obj | Objective name | Alk_Dept_Objective.objective_name |
| perspective | Perspective name | Alk_Perspective.perspective_name |

**Example**: If importing KPI Result, ensure:
- Employee code "EMP001" exists in Alk_Employee
- KPI name "Revenue Growth" exists in Alk_KPI

---

### Choice Field Values

**Semester Field** - Exact values only:
- `1st SEM`
- `2nd SEM`

**Month Field** - Exact values only:
- `1st`
- `2nd`
- `3rd`
- `4th`
- `5th`
- `final`

**KPI Type Field** - Integer values only:
- `1` (Bigger better)
- `2` (Smaller better)
- `3` (Mistake counting)

**Employee Level Field** - Integer values:
- `0` (Group Manager)
- `1` (Dept Manager)
- `2` (Regular, default)
- `3` (Restricted)
- `4` (Read-only)

---

## Common Scenarios

### Scenario 1: Bulk Add New Employees

1. **Export current employees** to get template
2. **Delete all rows** except header
3. **Add new employee rows**:
   ```
   emp_code,user,dept,dept_group,job_title,level
   EMP010,user10,Finance,Finance - 410,Accountant,2
   EMP011,user11,HR,HR - GA - 450,HR Specialist,2
   EMP012,user12,Plant Management,Plant Management - 460,Plant Engineer,2
   ```
4. **Ensure Users exist**: Create Django users first if needed
5. **Import file**

---

### Scenario 2: Bulk Update Employee Levels

1. **Export all employees**
2. **Update level column**:
   ```
   id,emp_code,user,dept,dept_group,job_title,level
   1,EMP001,john.doe,Finance,Finance - 410,Finance Manager,1
   2,EMP002,jane.smith,Finance,Finance - 410,Accountant,2
   ```
3. **Keep ID column** (for updating existing records)
4. **Import file**

---

### Scenario 3: Bulk Create KPI Results for New Semester

1. **Export previous semester results**
2. **Remove ID column** (to create new records)
3. **Update semester/month values**:
   ```
   year,semester,month,employee,kpi,weigth,min,max,target_set,target_input
   2025,2nd SEM,1st,EMP001,Revenue Growth,0.250,0.400,1.400,1.0000,1000000.0000
   2025,2nd SEM,1st,EMP001,Cost Reduction,0.200,0.400,1.400,800000.0000,800000.0000
   ```
4. **Leave achivement blank** (to be filled later)
5. **Import file**

---

### Scenario 4: Update Monthly Achievements

1. **Export current month results**
2. **Update achivement column**:
   ```
   id,year,semester,month,employee,kpi,achivement
   1,2025,1st SEM,1st,EMP001,Revenue Growth,1200000.0000
   2,2025,1st SEM,1st,EMP001,Cost Reduction,750000.0000
   ```
3. **Keep ID column** and other key fields
4. **Import file** (final_result auto-recalculates)

---

### Scenario 5: Mass Deactivate Old KPIs

1. **Export all KPIs**
2. **Update active column**:
   ```
   id,kpi_name,active
   5,Old Revenue Metric,FALSE
   6,Deprecated Cost KPI,FALSE
   ```
3. **Import file**

---

## Troubleshooting

### Error: "Row X: Alk_Employee with emp_code 'XXX' does not exist"

**Cause**: Referenced employee code not found in database

**Solution**:
1. Check employee code spelling (case-sensitive)
2. Ensure employee record exists in database
3. Import employees first, then KPI results

---

### Error: "Row X: Invalid choice for semester"

**Cause**: Semester value doesn't match exact choices

**Solution**: Use exactly `1st SEM` or `2nd SEM` (with space, uppercase)

**Wrong**: `1st Sem`, `first SEM`, `SEM1`  
**Correct**: `1st SEM`, `2nd SEM`

---

### Error: "Row X: Invalid value for kpi_type"

**Cause**: kpi_type must be integer 1, 2, or 3

**Solution**: Use numeric values only

**Wrong**: `Bigger better`, `Type 1`  
**Correct**: `1`, `2`, `3`

---

### Error: "Row X: This field cannot be null"

**Cause**: Required field is empty

**Solution**: Fill in all required fields for that model (see specifications above)

---

### Error: "Row X: Duplicate emp_code"

**Cause**: Trying to create employee with code that already exists

**Solution**:
1. Use ID column to update existing record
2. Or use different emp_code for new employee
3. Check if employee already exists in database

---

### Error: "Row X: User matching query does not exist"

**Cause**: Referenced username not found in Django User table

**Solution**:
1. Create Django User first via admin → Users
2. Check username spelling
3. Ensure user exists before importing employees

---

### Import Shows No Errors But Records Not Created

**Cause**: Clicked "Back" instead of "Confirm import"

**Solution**: After previewing, click **Confirm import** button to save changes

---

### Achievement Field Not Updating

**Cause**: KPI has `from_sap = True` (field is readonly)

**Solution**: 
1. Change kpi.from_sap to False
2. Or update via SAP integration only
3. Achievement is protected from manual edits for SAP KPIs

---

### Final Result Different Than Expected

**Cause**: Auto-calculated using calculation logic

**Solution**: 
1. Check calculation rules in [KPI Calculation Logic](kpi-calculation-logic.md)
2. Verify achievement, target_input, target_set values
3. Check kpi_type, percentage_cal flags
4. Review min/max thresholds

---

## Best Practices

### Before Import

1. ✅ **Backup Data**: Export current data before importing
2. ✅ **Use Template**: Export existing records to get correct format
3. ✅ **Test on Staging**: Test import on development environment first
4. ✅ **Validate Data**: Check values manually before import
5. ✅ **Check Foreign Keys**: Ensure all referenced records exist

### During Import

1. ✅ **Review Preview Carefully**: Check counts and errors
2. ✅ **Fix Errors**: Don't ignore validation errors
3. ✅ **Start Small**: Import small batches (50-100 records) first
4. ✅ **Monitor Progress**: Watch for success message

### After Import

1. ✅ **Verify Results**: Check records were created/updated correctly
2. ✅ **Check Calculations**: Verify final_result values make sense
3. ✅ **Export Again**: Export to confirm changes
4. ✅ **Document Changes**: Note what was imported and when

---

## Advanced Tips

### Excel Formula Preparation

Use Excel formulas to prepare data:

```excel
# Generate year column for 100 rows
=2025

# Copy semester value down
="1st SEM"

# Generate sequential month progression
=CHOOSE(MOD(ROW()-2,6)+1,"1st","2nd","3rd","4th","5th","final")

# Calculate weight from percentage
=25/100  # For 25%

# Concatenate employee code
="EMP"&TEXT(ROW()-1,"000")  # EMP001, EMP002, etc.
```

### Bulk Find-Replace

To update all references:
1. Open Excel file
2. Ctrl+H (Find and Replace)
3. Find: `Old Dept Name`
4. Replace with: `New Dept Name`
5. Replace All

### Filtering Before Export

Export only what you need:
1. Apply filters in admin interface
2. Export filtered results
3. Modify exported file
4. Import back

This is faster than modifying entire dataset.

---

## File Templates

### Employee Import Template

```csv
emp_code,user,dept,dept_group,job_title,level
EMP001,john.doe,Finance,Finance - 410,Finance Manager,1
EMP002,jane.smith,Finance,Finance - 410,Accountant,2
```

### KPI Import Template

```csv
kpi_name,dept_obj,perspective,kpi_type,from_sap,active,percentage_cal
Revenue Growth,Increase Revenue,Financial,1,FALSE,TRUE,FALSE
Cost Reduction,Reduce Costs,Financial,2,FALSE,TRUE,FALSE
```

### KPI Result Import Template

```csv
year,semester,month,employee,kpi,weigth,min,max,target_set,target_input,achivement
2025,1st SEM,1st,EMP001,Revenue Growth,0.250,0.400,1.400,1.0000,1000000.0000,1200000.0000
2025,1st SEM,1st,EMP001,Cost Reduction,0.200,0.400,1.400,800000.0000,800000.0000,750000.0000
```

---

**Last Updated**: December 30, 2025

For admin operations, see [Admin Guide](admin-guide.md).
