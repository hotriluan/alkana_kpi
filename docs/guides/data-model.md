# Data Model Documentation - Alkana KPI System

This document provides comprehensive documentation of the database schema, model relationships, and field specifications for the Alkana KPI Management System.

## Table of Contents
- [Overview](#overview)
- [Entity Relationship Diagram](#entity-relationship-diagram)
- [Core Models](#core-models)
- [Model Relationships](#model-relationships)
- [Field Specifications](#field-specifications)

## Overview

The Alkana KPI system uses 8 core models organized into three categories:

### Reference Data Models
1. **Alk_Dept** - Department definitions
2. **Alk_Dept_Group** - Department groupings
3. **Alk_Job_Title** - Job position titles
4. **Alk_Perspective** - KPI perspectives (Financial, Customer, etc.)
5. **Alk_Objective** - Department objectives

### Entity Models
6. **Alk_Employee** - Employee information and user linkage

### Operational Models
7. **Alk_KPI** - KPI definitions with calculation rules
8. **Alk_KPI_Result** - Actual KPI measurements and calculated scores

## Entity Relationship Diagram

```
┌──────────────────┐
│   Django User    │
│   (Built-in)     │
└────────┬─────────┘
         │ 1:1
         │
┌────────▼─────────────────────────────────────────┐
│              Alk_Employee                         │
│  ─────────────────────────────────────────────   │
│  • emp_code (PK)                                  │
│  • user_id (FK → User) [1:1]                      │
│  • dept_id (FK → Alk_Dept)                        │
│  • dept_group_id (FK → Alk_Dept_Group)            │
│  • job_title_id (FK → Alk_Job_Title)              │
│  • level (0-4 hierarchy)                          │
│  • name (auto-generated)                          │
└────────┬─────────────────────────────────────────┘
         │ 1:N
         │
┌────────▼─────────────────────────────────────────┐
│           Alk_KPI_Result                          │
│  ─────────────────────────────────────────────   │
│  • year, semester, month                          │
│  • employee_id (FK → Alk_Employee)                │
│  • kpi_id (FK → Alk_KPI)                          │
│  • weight, min, max, target_set                   │
│  • target_input, achievement                      │
│  • final_result (computed)                        │
└────────┬─────────────────────────────────────────┘
         │ N:1
         │
┌────────▼─────────────────────────────────────────┐
│               Alk_KPI                             │
│  ─────────────────────────────────────────────   │
│  • kpi_name                                       │
│  • dept_obj_id (FK → Alk_Dept_Objective)          │
│  • perspective_id (FK → Alk_Perspective)          │
│  • kpi_type (1, 2, or 3)                          │
│  • from_sap, percentage_cal, get_1_is_zero        │
│  • percent_display                                │
└──────┬───────────────────┬────────────────────────┘
       │ N:1                │ N:1
       │                    │
┌──────▼────────────┐  ┌────▼──────────────┐
│ Alk_Dept_Objective│  │  Alk_Perspective  │
│ ───────────────── │  │  ───────────────  │
│ • objective_name  │  │ • perspective_name│
│ • objective_abbrev│  │ • perspective_... │
└───────────────────┘  └───────────────────┘


┌──────────────────┐     ┌──────────────────┐
│    Alk_Dept      │     │ Alk_Dept_Group   │
│  ──────────────  │     │  ──────────────  │
│ • dept_name      │     │ • dept_group     │
│ • dept_abbrev    │     │ • dept_group_... │
│ • dept_group     │     └──────────────────┘
└──────────────────┘     
        │ 1:N
        │
┌───────▼──────────┐
│  Alk_Job_Title   │
│  ──────────────  │
│ • job_title      │
│ • job_title_...  │
└──────────────────┘
```

## Core Models

### 1. Alk_Dept (Department)

**Purpose**: Defines organizational departments.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-generated ID |
| dept_name | CharField(200) | Required | Full department name |
| dept_abbrev | CharField(50) | Required | Department abbreviation |
| dept_group | CharField(200) | Optional | Department group classification |

**Example Data**:
```python
Finance Department
  - dept_name: "Finance"
  - dept_abbrev: "FIN"
  - dept_group: "Finance - 410"
```

**Relationships**:
- One-to-Many with `Alk_Job_Title`
- One-to-Many with `Alk_Employee`

---

### 2. Alk_Dept_Group (Department Group)

**Purpose**: Groups departments into higher-level organizational units.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-generated ID |
| dept_group | CharField(200) | Required, Unique | Group identifier |
| dept_group_abbrev | CharField(50) | Optional | Group abbreviation |

**Example Data**:
```python
Finance - 410
HR - GA - 450
Plant Management - 460
```

**Relationships**:
- One-to-Many with `Alk_Employee`

---

### 3. Alk_Job_Title (Job Title)

**Purpose**: Defines employee job positions within departments.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-generated ID |
| job_title | CharField(200) | Required | Job title name |
| job_title_abbrev | CharField(50) | Optional | Title abbreviation |
| dept | ForeignKey | Required | Department assignment |

**Example Data**:
```python
Account Manager (Finance Department)
Finance Manager (Finance Department)
Plant Manager (Plant Management Department)
```

**Relationships**:
- Many-to-One with `Alk_Dept`
- One-to-Many with `Alk_Employee`

---

### 4. Alk_Perspective (KPI Perspective)

**Purpose**: Categorizes KPIs by business perspective (Balanced Scorecard methodology).

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-generated ID |
| perspective_name | CharField(200) | Required | Perspective name |
| perspective_abbrev | CharField(50) | Optional | Perspective abbreviation |

**Example Data**:
```python
Financial
Customer
Internal Process
Learning & Growth
```

**Relationships**:
- One-to-Many with `Alk_KPI`

---

### 5. Alk_Dept_Objective (Department Objective)

**Purpose**: Defines strategic objectives for departments, linked to KPIs.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-generated ID |
| objective_name | CharField(200) | Required | Objective description |
| objective_abbrev | CharField(50) | Optional | Objective abbreviation |

**Example Data**:
```python
Increase Revenue
Reduce Costs
Improve Customer Satisfaction
```

**Relationships**:
- One-to-Many with `Alk_KPI`

---

### 6. Alk_Employee (Employee)

**Purpose**: Central employee entity linking users to organizational structure and KPI results.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-generated ID |
| emp_code | CharField(50) | Required, Unique | Employee identifier |
| user | OneToOneField | Required | Django User linkage |
| dept | ForeignKey | Required | Department assignment |
| dept_group | ForeignKey | Required | Department group assignment |
| job_title | ForeignKey | Required | Job position |
| level | IntegerField | Default=2 | Permission level (0-4) |
| name | CharField(200) | Auto-generated | Full name from User |

**Level Hierarchy**:
- **Level 0**: Full admin access (can edit all records)
- **Level 1**: Manager access (can edit department records)
- **Level 2**: Regular employee (default, limited editing)
- **Level 3**: Restricted employee
- **Level 4**: Read-only employee

**Auto-Generated Fields**:
- `name` field is automatically populated from `User.first_name + User.last_name` on save

**Example Data**:
```python
Employee(
    emp_code="EMP001",
    user=User(username="john.doe"),
    dept=Finance,
    dept_group="Finance - 410",
    job_title="Finance Manager",
    level=1,
    name="John Doe"  # Auto-generated
)
```

**Relationships**:
- One-to-One with `User` (Django built-in)
- Many-to-One with `Alk_Dept`
- Many-to-One with `Alk_Dept_Group`
- Many-to-One with `Alk_Job_Title`
- One-to-Many with `Alk_KPI_Result`

---

### 7. Alk_KPI (KPI Definition)

**Purpose**: Defines KPI calculation rules and configuration.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-generated ID |
| kpi_name | CharField(200) | Required | KPI name/description |
| dept_obj | ForeignKey | Required | Department objective |
| perspective | ForeignKey | Required | KPI perspective |
| kpi_type | IntegerField | Required, Default=1 | Calculation type (1, 2, or 3) |
| from_sap | BooleanField | Default=False | Data source is SAP system |
| active | BooleanField | Default=True | KPI is active |
| percentage_cal | BooleanField | Default=False | Use percentage calculation mode |
| get_1_is_zero | BooleanField | Default=False | Special rule: achievement>0 → score=0 |
| percent_display | BooleanField | Default=False | Display result as percentage |

**KPI Type Choices**:
1. **Type 1 - Bigger is Better**: `result = achievement / target`
   - Example: Sales revenue, customer satisfaction score
   
2. **Type 2 - Smaller is Better**: `result = target / achievement`
   - Example: Cost reduction, cycle time
   
3. **Type 3 - Mistake Counting**: Inverted logic where 0 mistakes = max score
   - Example: Safety incidents, quality defects

**Calculation Flags**:
- **percentage_cal**: When True, uses `achievement/target_input` first, then applies ratio
- **get_1_is_zero**: Special rule where any achievement > 0 results in score = 0
- **percent_display**: Display final result as percentage in UI (formatting only)

**Example Data**:
```python
Revenue Growth (Type 1, bigger better)
  - kpi_type: 1
  - percentage_cal: True
  - target_set: 1.0 (100%)
  
Cost Reduction (Type 2, smaller better)
  - kpi_type: 2
  - percentage_cal: False
  
Safety Incidents (Type 3, mistake counting)
  - kpi_type: 3
  - get_1_is_zero: False
```

**Relationships**:
- Many-to-One with `Alk_Dept_Objective`
- Many-to-One with `Alk_Perspective`
- One-to-Many with `Alk_KPI_Result`

---

### 8. Alk_KPI_Result (KPI Result/Measurement)

**Purpose**: Records actual KPI measurements and automatically calculates weighted scores.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-generated ID |
| year | IntegerField | Required | Year (e.g., 2025) |
| semester | CharField(7) | Required | "1st SEM" or "2nd SEM" |
| month | CharField(6) | Required | "1st", "2nd", "3rd", "4th", "5th", "final" |
| employee | ForeignKey | Required | Employee assignment |
| kpi | ForeignKey | Required | KPI definition |
| weight | Decimal(20,3) | Required | Weight/importance (0.0-1.0 typical) |
| min | Decimal(20,3) | Default=0.4 | Minimum threshold (below = 0 score) |
| max | Decimal(20,3) | Default=1.4 | Maximum threshold (cap at max) |
| target_set | Decimal(20,4) | Required | Target ratio or percentage |
| target_input | Decimal(20,4) | Optional | Actual target value (auto-set if not percentage_cal) |
| achievement | Decimal(20,4) | Optional | Actual achievement value |
| final_result | Decimal(20,3) | Auto-calculated | **Weighted score (read-only)** |
| active | BooleanField | Default=True | Record is active |

**Time Period Structure**:
- Each year has 2 semesters (1st SEM, 2nd SEM)
- Each semester has 6 periods: 5 months (1st-5th) + final

**Threshold Logic**:
- **min** (default 0.4): If performance ratio < min → score = 0
- **max** (default 1.4): If performance ratio > max → score = max × weight

**Auto-Save Behavior**:
- If `kpi.percentage_cal = False`, then `target_input = target_set` (auto-set)
- `final_result` is always calculated before saving (read-only)

**Example Data**:
```python
KPI_Result(
    year=2025,
    semester="1st SEM",
    month="1st",
    employee=John_Doe,
    kpi=Revenue_Growth_KPI,
    weight=0.300,  # 30% of total score
    min=0.4,       # Below 40% performance = 0 points
    max=1.4,       # Cap at 140% performance
    target_set=1.0,       # 100% target
    target_input=1000000, # $1M target
    achievement=1200000,  # $1.2M achieved
    final_result=0.360    # Auto-calculated: (1.2M/1M) * 0.300 = 0.360
)
```

**Relationships**:
- Many-to-One with `Alk_Employee`
- Many-to-One with `Alk_KPI`

**Calculation Logic**:
See [KPI Calculation Logic](kpi-calculation-logic.md) for detailed formula documentation.

---

## Model Relationships

### Relationship Summary

| Relationship | Type | Description |
|--------------|------|-------------|
| User ↔ Alk_Employee | One-to-One | Each Django user linked to one employee |
| Alk_Dept → Alk_Job_Title | One-to-Many | Department has multiple job titles |
| Alk_Dept → Alk_Employee | One-to-Many | Department has multiple employees |
| Alk_Dept_Group → Alk_Employee | One-to-Many | Dept group has multiple employees |
| Alk_Job_Title → Alk_Employee | One-to-Many | Job title has multiple employees |
| Alk_Perspective → Alk_KPI | One-to-Many | Perspective has multiple KPIs |
| Alk_Dept_Objective → Alk_KPI | One-to-Many | Objective has multiple KPIs |
| Alk_Employee → Alk_KPI_Result | One-to-Many | Employee has multiple KPI results |
| Alk_KPI → Alk_KPI_Result | One-to-Many | KPI has multiple results (across employees/periods) |

### Cascade Deletion Rules

All ForeignKey relationships use `on_delete=models.CASCADE`:

- Deleting a **Department** → Deletes all job titles and employees in that department
- Deleting an **Employee** → Deletes all KPI results for that employee
- Deleting a **KPI** → Deletes all KPI results using that KPI definition
- Deleting a **User** → Deletes the linked employee record

**⚠️ WARNING**: Cascade deletions can affect large amounts of data. Use caution.

---

## Field Specifications

### Common Field Patterns

#### CharField Lengths
- **Short codes/abbreviations**: CharField(50) - Used for dept_abbrev, emp_code, etc.
- **Names/descriptions**: CharField(200) - Used for kpi_name, dept_name, etc.

#### Decimal Precision
- **Weights and ratios**: Decimal(20, 3) - 3 decimal places, supports 0.000 to 999,999,999,999,999,999.999
- **Targets and achievements**: Decimal(20, 4) - 4 decimal places for higher precision

#### Boolean Defaults
- Most boolean fields default to `False` or `True` based on common usage
- `active` fields default to `True` (records are active by default)

### Constraints and Validation

#### Unique Constraints
- `Alk_Employee.emp_code` - Must be unique across all employees
- `Alk_Dept_Group.dept_group` - Must be unique across all groups
- `User.username` - Django built-in unique constraint

#### Required vs Optional
- **Required fields**: All ForeignKeys, year, semester, month, kpi_name, dept_name
- **Optional fields**: target_input, achievement (can be null until data is entered)

#### Default Values
- `level`: 2 (Regular employee)
- `min`: 0.4 (40% minimum threshold)
- `max`: 1.4 (140% maximum threshold)
- `kpi_type`: 1 (Bigger is better)
- All boolean flags: False (except `active` = True)

---

## Database Indexes

### Automatic Indexes (via ForeignKey)
Django automatically creates indexes on all ForeignKey fields for query optimization.

### Recommended Custom Indexes

Consider adding these indexes for performance:

```python
# In models.py Meta class
class Alk_KPI_Result(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['year', 'semester', 'month']),
            models.Index(fields=['employee', 'year', 'semester']),
            models.Index(fields=['kpi', 'year']),
        ]
```

---

## Data Integrity Rules

### Business Logic Constraints

1. **Employee-User Linkage**: Each employee must be linked to exactly one Django user
2. **Level Hierarchy**: Employee levels must be 0-4 (enforced in admin)
3. **Semester-Month Combinations**: Valid combinations only (handled by choices)
4. **Weight Validation**: Weights should sum to 1.0 per employee/semester (validated in admin)
5. **Threshold Logic**: min < max (should be validated)

### Calculation Dependencies

1. **target_input auto-set**: When `kpi.percentage_cal = False`, `target_input` is copied from `target_set`
2. **final_result auto-calculated**: Always recalculated on save (cannot be manually edited)
3. **name auto-generated**: Employee name is synced from User model on save

---

## Sample SQL Queries

### Get all KPI results for an employee in a semester
```sql
SELECT 
    r.year,
    r.semester,
    r.month,
    k.kpi_name,
    r.target_input,
    r.achivement,
    r.final_result
FROM kpi_app_alk_kpi_result r
JOIN kpi_app_alk_kpi k ON r.kpi_id = k.id
JOIN kpi_app_alk_employee e ON r.employee_id = e.id
WHERE e.emp_code = 'EMP001'
  AND r.year = 2025
  AND r.semester = '1st SEM'
ORDER BY r.month;
```

### Calculate total weighted score for an employee
```sql
SELECT 
    e.emp_code,
    e.name,
    r.year,
    r.semester,
    r.month,
    SUM(r.final_result) as total_score
FROM kpi_app_alk_kpi_result r
JOIN kpi_app_alk_employee e ON r.employee_id = e.id
WHERE r.year = 2025
  AND r.semester = '1st SEM'
  AND r.month = 'final'
GROUP BY e.emp_code, e.name, r.year, r.semester, r.month;
```

### Get KPI definitions by department
```sql
SELECT 
    d.dept_name,
    o.objective_name,
    p.perspective_name,
    k.kpi_name,
    k.kpi_type
FROM kpi_app_alk_kpi k
JOIN kpi_app_alk_dept_objective o ON k.dept_obj_id = o.id
JOIN kpi_app_alk_perspective p ON k.perspective_id = p.id
JOIN kpi_app_alk_job_title jt ON jt.dept_id = (
    SELECT dept_id FROM kpi_app_alk_employee WHERE id = 1 LIMIT 1
)
JOIN kpi_app_alk_dept d ON jt.dept_id = d.id
WHERE k.active = TRUE
ORDER BY d.dept_name, k.kpi_name;
```

---

## Migration History

Key database changes tracked in `kpi_app/migrations/`:

- **0001_initial.py**: Initial schema creation
- **0007**: Added `get_1_is_zero` and `is_percentage` flags
- **0011**: Renamed `is_percentage` to `percentage_cal`
- **0014**: Added `Alk_KPI_Result` model
- **0023**: Added `percent_display` flag
- **0024**: Added `active` flag to KPI results
- **0026**: Modified employee level field
- **0027**: Modified dept_group field (latest)

---

**Last Updated**: December 30, 2025

For calculation logic details, see [KPI Calculation Logic](kpi-calculation-logic.md).
