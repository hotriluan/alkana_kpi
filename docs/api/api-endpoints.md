# API Endpoints - Alkana KPI System

This document describes the available URLs and views in the Alkana KPI application.

## Table of Contents
- [Overview](#overview)
- [Authentication Endpoints](#authentication-endpoints)
- [User Endpoints](#user-endpoints)
- [Report Endpoints](#report-endpoints)
- [Admin Endpoints](#admin-endpoints)
- [URL Patterns](#url-patterns)

## Overview

The application uses Django's URL routing with both function-based views and the Django Admin interface.

**Base URL**: `http://yourdomain.com/` or `https://yourdomain.com/`

**Authentication**: All endpoints except login require authenticated users (@login_required decorator).

## Authentication Endpoints

### Login

**URL**: `/login/` or `/accounts/login/`  
**Method**: GET, POST  
**View**: `kpi_app.views.user_login`  
**Template**: `registration/login.html`  
**Authentication**: None (public)

**Purpose**: User authentication

**GET Parameters**: None

**POST Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| username | string | Yes | User's username |
| password | string | Yes | User's password |

**Response**:
- **Success**: Redirect to `/home/`
- **Failure**: Re-render login form with errors

**Example**:
```python
# POST /login/
{
    'username': 'john.doe',
    'password': 'password123'
}
```

---

### Logout

**URL**: `/logout/` or `/accounts/logout/`  
**Method**: GET, POST  
**View**: `kpi_app.views.user_logout`  
**Authentication**: Required

**Purpose**: Log out current user and clear session

**Response**: Redirect to `/login/`

**Example**:
```
GET /logout/
→ Redirects to /login/
```

---

## User Endpoints

### User Profile

**URL**: `/profile/`  
**Method**: GET, POST  
**View**: `kpi_app.views.profile`  
**Template**: `kpi_app/profile.html`  
**Authentication**: Required (@login_required)

**Purpose**: View and update user profile information

**GET**: Display profile form with current user data

**POST Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| first_name | string | Yes | User's first name |
| last_name | string | Yes | User's last name |
| email | string | Yes | User's email address |
| old_password | string | Optional | Current password (for password change) |
| new_password1 | string | Optional | New password |
| new_password2 | string | Optional | New password confirmation |

**Response**:
- **Success**: Redirect to `/profile/` with success message
- **Validation Error**: Re-render form with error messages

**Example**:
```python
# POST /profile/
{
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john.doe@company.com',
    'old_password': 'oldpass123',
    'new_password1': 'newpass456',
    'new_password2': 'newpass456'
}
```

**Permissions**:
- User can only edit their own profile
- Password change requires old password verification

---

## Report Endpoints

### Home / KPI Report

**URL**: `/home/`  
**Method**: GET  
**View**: `kpi_app.views.home`  
**Template**: `kpi_app/home.html`  
**Authentication**: Required (@login_required)

**Purpose**: Display KPI results report with filtering and pagination

**GET Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| year | integer | No | Filter by year (e.g., 2025) |
| semester | string | No | Filter by semester ("1st SEM" or "2nd SEM") |
| month | string | No | Filter by month ("1st", "2nd", ..., "final") |
| user_id | string | No | Filter by username (partial match) |
| name | string | No | Filter by employee name (partial match) |
| page | integer | No | Page number for pagination (default: 1) |

**Response**: HTML page with report data

**Data Returned**:
- Year, semester, month
- Employee username, name, department
- Subtotal (sum of final_result for grouped records)
- Pagination: 20 records per page

**Access Control**:
- **Superuser**: Can see all KPI results
- **Regular User**: Can only see results from their department

**Example**:
```
GET /home/?year=2025&semester=1st%20SEM&month=1st&page=1
```

**Response Context**:
```python
{
    'user_dept': [<QuerySet of departments>],
    'report_data': <Paginator Page object>,
    'filters': {
        'year': '2025',
        'semester': '1st SEM',
        'month': '1st',
        'user_id': '',
        'name': '',
    }
}
```

---

### Export KPI Results to Excel

**URL**: `/export-alk-kpi-result/`  
**Method**: GET  
**View**: `kpi_app.views.export_alk_kpi_result`  
**Authentication**: Required (@login_required)

**Purpose**: Export filtered KPI results to Excel file

**GET Parameters**: Same as `/home/` endpoint
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| year | integer | No | Filter by year |
| semester | string | No | Filter by semester |
| month | string | No | Filter by month |
| user_id | string | No | Filter by username |
| name | string | No | Filter by employee name |

**Response**: Excel file download (.xlsx)

**Filename Format**: `KPI_Results_<timestamp>.xlsx`

**Exported Columns**:
- Year
- Semester
- Month
- Username
- Employee Name
- Department
- Subtotal (sum of final_result)

**Example**:
```
GET /export-alk-kpi-result/?year=2025&semester=1st%20SEM
→ Downloads: KPI_Results_2025-12-30_14-30-45.xlsx
```

**Access Control**: Same as `/home/` - users can only export data they have access to view

---

### Manage KPI Results

**URL**: `/manage/`  
**Method**: GET, POST  
**View**: `kpi_app.views.manage_kpi_result`  
**Template**: `manage.html`  
**Authentication**: Required (@login_required)

**Purpose**: Bulk activate/deactivate KPI results

**GET**: Display management interface

**POST Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| result_ids | list | Yes | List of KPI result IDs to modify |
| action | string | Yes | "activate" or "deactivate" |

**Actions**:
- **activate**: Sets `active=True` for selected results
- **deactivate**: Sets `active=False` for selected results

**Response**:
- **Success**: Redirect with success message
- **Error**: Re-render with error message

**Example**:
```python
# POST /manage/
{
    'result_ids': [1, 2, 3, 5],
    'action': 'deactivate'
}
```

---

## Admin Endpoints

### Django Admin Interface

**URL**: `/admin/`  
**Method**: GET, POST  
**View**: Django Admin Site  
**Authentication**: Required (staff status)

**Purpose**: Main administration interface

**Available Models**:
- `/admin/auth/user/` - User management
- `/admin/auth/group/` - Group management
- `/admin/kpi_app/alk_dept/` - Departments
- `/admin/kpi_app/alk_dept_group/` - Department groups
- `/admin/kpi_app/alk_employee/` - Employees
- `/admin/kpi_app/alk_job_title/` - Job titles
- `/admin/kpi_app/alk_kpi/` - KPIs
- `/admin/kpi_app/alk_kpi_result/` - KPI Results
- `/admin/kpi_app/alk_objective/` - Objectives
- `/admin/kpi_app/alk_perspective/` - Perspectives

**Permissions**: See [Permission Matrix](../guides/permission-matrix.md)

---

## URL Patterns

### Application URL Structure

**Root URL** (`/`):
```python
def redirect_root(request):
    return HttpResponseRedirect('/admin/')
```
Root redirects to `/admin/`

**KPI App URLs** (from `kpi_app/urls.py`):
```python
urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('accounts/logout/', views.user_logout, name='accounts_logout'),
    path('export-alk-kpi-result/', views.export_alk_kpi_result, name='export_alk_kpi_result'),
    path('manage/', views.manage_kpi_result, name='manage_kpi_result'),
]
```

**Main Project URLs** (from `alkana_kpi/urls.py`):
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_root),
    path('', include('kpi_app.urls')),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout/', views.user_logout, name='logout'),
]
```

---

## URL Naming Convention

**Named URLs** for use in templates and redirects:

| URL Name | Path | Purpose |
|----------|------|---------|
| `home` | `/home/` | KPI report homepage |
| `login` | `/login/` or `/accounts/login/` | User login |
| `logout` | `/logout/` or `/accounts/logout/` | User logout |
| `accounts_logout` | `/accounts/logout/` | Alternate logout |
| `profile` | `/profile/` | User profile |
| `export_alk_kpi_result` | `/export-alk-kpi-result/` | Export to Excel |
| `manage_kpi_result` | `/manage/` | Manage KPI results |

**Usage in Templates**:
```django
<a href="{% url 'home' %}">Home</a>
<a href="{% url 'profile' %}">My Profile</a>
<a href="{% url 'logout' %}">Logout</a>
```

**Usage in Views**:
```python
from django.shortcuts import redirect

return redirect('home')
return redirect('login')
```

---

## HTTP Status Codes

| Code | Meaning | When Returned |
|------|---------|---------------|
| 200 | OK | Successful GET request |
| 302 | Redirect | After successful POST, logout, or authentication |
| 403 | Forbidden | User lacks permission for resource |
| 404 | Not Found | URL doesn't exist |
| 500 | Server Error | Application error |

---

## Request/Response Examples

### Example 1: Login Flow

**Request**:
```http
POST /login/ HTTP/1.1
Host: yourdomain.com
Content-Type: application/x-www-form-urlencoded

username=john.doe&password=securepass123
```

**Response** (Success):
```http
HTTP/1.1 302 Found
Location: /home/
Set-Cookie: sessionid=abc123...; HttpOnly; Secure
```

---

### Example 2: View KPI Report with Filters

**Request**:
```http
GET /home/?year=2025&semester=1st%20SEM&month=1st&page=1 HTTP/1.1
Host: yourdomain.com
Cookie: sessionid=abc123...
```

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head><title>KPI Report</title></head>
<body>
    <!-- Report table with filtered results -->
    <!-- Pagination controls -->
</body>
</html>
```

---

### Example 3: Export to Excel

**Request**:
```http
GET /export-alk-kpi-result/?year=2025&semester=1st%20SEM HTTP/1.1
Host: yourdomain.com
Cookie: sessionid=abc123...
```

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="KPI_Results_2025-12-30_14-30-45.xlsx"

[Excel file binary data]
```

---

## Security Considerations

### CSRF Protection

All POST requests require CSRF token:

```django
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### Authentication Required

Most endpoints require login:
```python
@login_required
def profile(request):
    # View code
```

Unauthenticated users redirected to `/login/`

### Permission Checks

Views implement permission checks:
- `/home/`: Filters results by user's department (unless superuser)
- `/profile/`: Users can only edit own profile
- `/admin/`: Requires staff status and appropriate permissions

---

## Future API Endpoints

**Potential additions** for future versions:

- **REST API**: JSON endpoints for mobile/external integration
  - `GET /api/kpi-results/` - List KPI results
  - `POST /api/kpi-results/` - Create KPI result
  - `PUT /api/kpi-results/{id}/` - Update KPI result
  - `DELETE /api/kpi-results/{id}/` - Delete KPI result

- **Dashboard API**: Aggregated statistics
  - `GET /api/dashboard/stats/` - Summary statistics
  - `GET /api/dashboard/charts/` - Chart data

- **Notification Endpoints**: User notifications
  - `GET /api/notifications/` - List notifications
  - `POST /api/notifications/{id}/mark-read/` - Mark as read

Consider using **Django REST Framework** for API development.

---

**Last Updated**: December 30, 2025

For view implementation details, see [kpi_app/views.py](../../kpi_app/views.py).
