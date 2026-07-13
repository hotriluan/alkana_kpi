# Data Locking Mechanism Implementation Plan

## Goal Description
Implement a "Hard Lock" mechanism to prevent modification of KPI results by Level 2 (End Users) after they have been finalized or approved. This ensures data integrity for historical records (past 6 months) and allows Managers (Level 1) or Admins to control the editability of data.

## User Review Required
> [!IMPORTANT]
> This change involves a schema migration for `Alk_KPI_Result`. A backup of the database is recommended before applying the migration, although the default value `False` for `is_locked` should ensure no immediate data loss or access change.

## Proposed Changes

### kpi_app
#### [MODIFY] [models.py](file:///c:/dev/alkana_kpi/kpi_app/models.py)
- **Class `Alk_KPI_Result`**:
    - Add `is_locked` (BooleanField, default=False).
    - Add `verbose_name="Locked / Finalized"`.

#### [MODIFY] [admin.py](file:///c:/dev/alkana_kpi/kpi_app/admin.py)
- **Class `Alk_KPI_ResultAdmin`**:
    - Add custom admin actions:
        - `lock_kpi_results`: Sets `is_locked=True`.
        - `unlock_kpi_results`: Sets `is_locked=False`.
        - **Permission Logic**:
            - **Superuser**: Can lock/unlock ALL records.
            - **Level 0 (Group Manager)**: Can lock/unlock records for employees in the same `alk-dept.group`.
            - **Level 1 (Dept Manager)**: Can lock/unlock records for employees in the same `alk-dept`.
            - **Level 2**: Cannot lock/unlock.
    - Override `get_readonly_fields`:
        - If `obj.is_locked` is True and User Level is >= 2, make all fields read-only.

## Verification Plan

### Automated Tests
- Since this project relies heavily on the Admin interface, automated testing might be limited to unit tests for the model and admin permissions if a test suite exists.
- We will rely primarily on **Manual Verification**.

### Manual Verification
1.  **Schema Check**: Verify `is_locked` column exists in the database.
2.  **Admin UI**:
    - Login as Superuser/Manager.
    - Check "Locked / Finalized" checkbox availability.
    - Test "Bulk Lock" and "Bulk Unlock" actions.
3.  **Permission Check**:
    - Lock a record.
    - Login as Level 2 User (or simulate by checking logic).
    - Verify that fields are read-only for the locked record.
    - Verify that fields are editable for an unlocked record.
4.  **Historical Data**: Ensure existing 6-months data defaults to `is_locked=False` (Unlocked) and is still accessible.
