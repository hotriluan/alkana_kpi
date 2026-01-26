# Database Schema Documentation

Generated from Django models with sample data.

## Table: alk_dept (`kpi_app_alk_dept`)
- **Description**: alk_dept(dept_id, dept_name, group, active)
- **Columns**:
    - `dept_id` (AutoField): PK, Unique
    - `dept_name` (CharField): Unique
    - `group` (CharField): Null, Default: 
    - `active` (BooleanField): Default: True

- **Sample Data** (First 5 rows):
| dept_id | dept_name | group | active |
| --- | --- | --- | --- |
| 2 | Finance | Gunawan | True |
| 3 | HR & GA | Nhu | True |
| 4 | Plant Management | Gunawan | True |
| 5 | Product Development | Michel | True |
| 58 | Product Development Retail | Gunawan | True |

---
## Table: alk_job_title (`kpi_app_alk_job_title`)
- **Description**: alk_job_title(job_id, job_title, active)
- **Columns**:
    - `job_id` (AutoField): PK, Unique
    - `job_title` (CharField): Unique
    - `active` (BooleanField): Default: True

- **Sample Data** (First 5 rows):
| job_id | job_title | active |
| --- | --- | --- |
| 251 | Account Manager | True |
| 252 | AR Officer | True |
| 253 | Banking & AP Officer | True |
| 254 | Cashier | True |
| 258 | Chief Accountant | True |

---
## Table: alk_perspective (`kpi_app_alk_perspective`)
- **Description**: alk_perspective(perspective_id, perspective_name, active)
- **Columns**:
    - `perspective_id` (AutoField): PK, Unique
    - `perspective_name` (CharField): Unique
    - `active` (BooleanField): Default: True

- **Sample Data** (First 5 rows):
| perspective_id | perspective_name | active |
| --- | --- | --- |
| 29 | Customer Perspective | True |
| 30 | DCP with 8D | True |
| 31 | Financial Perspective | True |
| 32 | Internal Process Perspective | True |
| 33 | Learning & Growth Perspective | True |

---
## Table: alk_dept_objective (`kpi_app_alk_dept_objective`)
- **Description**: alk_dept_objective(objective_id, objective_name, active)
- **Columns**:
    - `objective_id` (AutoField): PK, Unique
    - `objective_name` (CharField): Unique
    - `active` (BooleanField): Default: True

- **Sample Data** (First 5 rows):
| objective_id | objective_name | active |
| --- | --- | --- |
| 52 | % AR Collection  | True |
| 53 | Accident Rate & Fire Protection | True |
| 54 | AR Collection  | True |
| 55 | Budget accuracy | True |
| 56 | Cash Flow | True |

---
## Table: alk_dept_group (`kpi_app_alk_dept_group`)
- **Description**: alk_dept_group(group_id, group_name, active)
- **Columns**:
    - `group_id` (AutoField): PK, Unique
    - `group_name` (CharField): Unique
    - `active` (BooleanField): Default: True

- **Sample Data** (First 5 rows):
| group_id | group_name | active |
| --- | --- | --- |
| 41 | Chi - 999 | True |
| 42 | Finance - 410 | True |
| 43 | General Mgnt - 400 | True |
| 44 | HR - GA - 450 | True |
| 45 | Hung - 444 | True |

---
## Table: alk_employee (`kpi_app_alk_employee`)
- **Description**: alk_employee(id, user_id, name, job_title, dept, dept_gr, level, active)
- **Columns**:
    - `id` (BigAutoField): PK, Unique
    - `user_id` (ForeignKey): 
    - `name` (CharField): Default: 
    - `job_title` (ForeignKey): 
    - `dept` (ForeignKey): 
    - `dept_gr` (ForeignKey): 
    - `level` (IntegerField): 
    - `active` (BooleanField): Default: True

- **Sample Data** (First 5 rows):
| id | user_id | name | job_title | dept | dept_gr | level | active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 916 | f654 | Bùi Thị Kim Hương | Banking & AP Officer | Finance | Finance - 410 | 3 | True |
| 914 | f051 | Hồ Trí Luân | IT Supervisor | Finance | Finance - 410 | 2 | True |
| 926 | p138 | Nguyễn Như Thị Ngọc Mỹ | AR Officer | Finance | Finance - 410 | 3 | True |
| 915 | f388 | Nguyễn Thị An Tiến | Finance Manager | Finance | Finance - 410 | 1 | True |
| 924 | p039 | Phạm Thị Gương Em | Cashier | Finance | Finance - 410 | 3 | True |

---
## Table: alk_kpi (`kpi_app_alk_kpi`)
- **Description**: alk_kpi(id, kpi_name, dept_obj, perspective, kpi_type, from_sap, active, percentage_cal, get_1_is_zero, percent_display)
- **Columns**:
    - `id` (BigAutoField): PK, Unique
    - `kpi_name` (CharField): 
    - `dept_obj` (ForeignKey): 
    - `perspective` (ForeignKey): 
    - `kpi_type` (IntegerField): Default: 1
    - `from_sap` (BooleanField): Default: False
    - `active` (BooleanField): Default: True
    - `percentage_cal` (BooleanField): Default: False
    - `get_1_is_zero` (BooleanField): Default: False
    - `percent_display` (BooleanField): Null, Default: False

- **Sample Data** (First 5 rows):
| id | kpi_name | dept_obj | perspective | kpi_type | from_sap | active | percentage_cal | get_1_is_zero | percent_display |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1422 | % AR Collection | % AR Collection  | Financial Perspective | 1 | True | True | True | False | False |
| 1423 | % of completion of the planned machinery inspec... | SHE Performance | Learning & Growth Perspective | 1 | False | True | False | False | True |
| 1424 | % of POSTO date to POS date in 1 day (avearage) | Order Fulfillment | Internal Process Perspective | 1 | False | True | False | False | True |
| 1425 | % of released POS vs total POSTO | Order Fulfillment | Internal Process Perspective | 1 | False | True | False | False | True |
| 1426 | % of Return | Customer Satisfaction | Customer Perspective | 2 | False | True | True | False | False |

---
## Table: alk_kpi_result (`kpi_app_alk_kpi_result`)
- **Description**: alk_kpi_result(id, year, semester, employee, kpi, weigth, min, target_set, max, target_input, achivement, month, final_result, active)
- **Columns**:
    - `id` (BigAutoField): PK, Unique
    - `year` (IntegerField): 
    - `semester` (CharField): 
    - `employee` (ForeignKey): 
    - `kpi` (ForeignKey): 
    - `weigth` (DecimalField): Null
    - `min` (DecimalField): Default: 0.4
    - `target_set` (DecimalField): Null
    - `max` (DecimalField): Default: 1.4
    - `target_input` (DecimalField): Null
    - `achivement` (DecimalField): Null
    - `month` (CharField): 
    - `final_result` (DecimalField): Null
    - `active` (BooleanField): Default: True

- **Sample Data** (First 5 rows):
| id | year | semester | employee | kpi | weigth | min | target_set | max | target_input | achivement | month | final_result | active |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5402 | 2025 | 2nd SEM | f654 - Banking & AP Officer | AP Days  | 0.300 | 0.000 | 66.0000 | 1.400 | 66.0000 | 58.0000 | 1st | 0.264 | True |
| 6716 | 2025 | 2nd SEM | f654 - Banking & AP Officer | AP Days  | 0.300 | 0.000 | 66.0000 | 1.400 | 66.0000 | 67.0000 | 2nd | 0.305 | True |
| 8030 | 2025 | 2nd SEM | f654 - Banking & AP Officer | AP Days  | 0.300 | 0.000 | 66.0000 | 1.400 | 66.0000 | 68.0000 | 3rd | 0.309 | True |
| 9344 | 2025 | 2nd SEM | f654 - Banking & AP Officer | AP Days  | 0.300 | 0.000 | 66.0000 | 1.400 | 66.0000 | None | 4th | 0.000 | True |
| 10658 | 2025 | 2nd SEM | f654 - Banking & AP Officer | AP Days  | 0.300 | 0.000 | 66.0000 | 1.400 | 66.0000 | None | 5th | 0.000 | True |

---
