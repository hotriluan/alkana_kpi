# Implementation Plan - Employee User Portal

**Goal**: Decouple End Users (Level 2) from Django Admin by creating a modern, distinct "Employee Portal" using Bootstrap 5 and HTMX.

> [!IMPORTANT]
> **Design Philosophy (UI-UX-PRO-MAX)**: The interface will use a "Glassmorphism" inspired design with soft shadows, rounded corners, and smooth transitions to provide a premium feel, distinguishing it sharply from the rigid Django Admin interface.

## User Review Required
- **Refactoring Strategy**: We will move `admin.py` views (if any custom ones exist) and create a new `views/` package. This changes the project structure slightly.
- **URL Namespace**: New URLs will be under `/portal/`.

## Proposed Changes

### 1. Project Structure Refactoring
We will convert `kpi_app/views.py` (if it exists or is used) into a package to separate concerns.

#### [NEW] [kpi_app/views/__init__.py](file:///c:/dev/alkana_kpi/kpi_app/views/__init__.py)
Expose views for easier importing.

#### [NEW] [kpi_app/views/portal_views.py](file:///c:/dev/alkana_kpi/kpi_app/views/portal_views.py)
Contains all logic for the portal:
- `portal_login`: Custom login view.
- `portal_dashboard`: Analytics and Charts.
- `input_form`: The main data entry grid.
- `save_kpi_result`: HTMX endpoint for saving.

### 2. URL Configuration
#### [MODIFY] [kpi_app/urls.py](file:///c:/dev/alkana_kpi/kpi_app/urls.py)
- Register `/portal/` namespace.
- Add routes for login, dashboard, input, and htmx actions.

### 3. Frontend Implementation (UI-UX-PRO-MAX)
All templates will reside in `kpi_app/templates/kpi_app/portal/`.

#### [NEW] [base.html](file:///c:/dev/alkana_kpi/kpi_app/templates/kpi_app/portal/base.html)
- **Layout**: Navbar with User Profile dropdown.
- **Assets**: Bootstrap 5.3 (CDN), HTMX (CDN), Google Fonts (Inter/Poppins), FontAwesome/Bootstrap Icons.
- **Theme**: Light mode with subtle gradients.

#### [NEW] [dashboard.html](file:///c:/dev/alkana_kpi/kpi_app/templates/kpi_app/portal/dashboard.html)
- **Hero Section**: Greeting card with "Current Month Completion" status.
- **Charts**: `Chart.js` bar chart showing KPI performance trend (Last 6 months).
- **Recent Activity**: List of recently updated KPIs.

#### [NEW] [input_form.html](file:///c:/dev/alkana_kpi/kpi_app/templates/kpi_app/portal/input_form.html)
- **Structure**: Responsive card layout (Desktop: Table, Mobile: Card list).
- **Navigation**: Month/Year/Semester selectors.

#### [NEW] [partials/kpi_row.html](file:///c:/dev/alkana_kpi/kpi_app/templates/kpi_app/portal/partials/kpi_row.html)
- **Smart Input**:
    - Uses HTMX for auto-saving (`hx-post`, `hx-trigger="change delay:500ms"`).
    - **Validation**: Backward feedback (Red border/Warning text) if input is suspicious (e.g. >1.5 for percentage).
- **Status Indicator**:
    - **Approved**: Green Text + Lock Icon + Read-only.
    - **Pending**: Editable input field.

### 4. Backend Logic & Validation
In `portal_views.py`:
- **Security**: Decorator `@login_required` + Global check `if user.level != 2: redirect('admin')`.
- **Encryption**: Standard Django CSRF protection for HTMX.
- **Smart Validation**:
    - Detect `kpi_type == 1` (Percentage).
    - If user enters `10`, save as `10` but return a UI warning "Did you mean 0.1?". (Alternatively, auto-convert logic if validated).
    - *Decision*: We will warn, not auto-convert, to be safe.

## Verification Plan

### Automated Tests
- Test Login redirection logic (Level 0 vs Level 2).
- Test Access Control (Level 2 cannot access Admin).

### Manual Verification
1. **Login**: Login as a Level 2 User (`emp_level2`). Verify redirect to Portal.
2. **Dashboard**: Check chart rendering.
3. **Data Entry**:
    - Enter a valid number -> Check "Saved" indicator (Green tick).
    - Enter "10" for percentage -> Check Warning message.
    - Refresh page -> Check data persistence.
4. **Locking**:
    - Login as Manager -> Approve a record.
    - Login as Level 2 -> Verify record is Locked (Read-only) in Portal.
