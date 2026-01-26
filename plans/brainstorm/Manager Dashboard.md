Phase 3 (Revised): Implementation Plan - Manager Dashboard
**Project:** Alkana KPI System
**Objective:** Create a dedicated "Command Center" for Level 1 Managers to monitor team progress, spot anomalies, and track approval status without digging into Excel files or Admin grids.
**Target Audience:** Level 1 (Department Managers) & Level 0 (Group Managers).

---

## 1. Technical Architecture

**URL:** `/portal/manager/`
**Tech Stack:** * **Backend:** Django View (Optimized with `prefetch_related`).
* **Frontend:** Bootstrap 5 (Layout), Chart.js (Visuals).
* **Access Control:** Strict check `if user.level <= 1`.

---

## 2. Implementation Logic

### A. View Logic (`kpi_app/views/portal_views.py`)

We need a view that aggregates data efficiently.

```python
from django.db.models import Count, Avg, Q
from django.contrib.auth.decorators import login_required
from kpi_app.models import Alk_Employee, Alk_KPI_Result

@login_required
def manager_dashboard(request):
    # 1. Security Check
    current_employee = getattr(request.user, 'alk_employee', None)
    if not current_employee or current_employee.level > 1:
        return redirect('portal_dashboard') # Redirect unauthorized users back to their own page

    # 2. Define Scope (Department vs Group)
    # Using logic from Permission Matrix
    if current_employee.level == 0:
        team_scope = Alk_Employee.objects.filter(dept_group=current_employee.dept_group)
    else: # Level 1
        team_scope = Alk_Employee.objects.filter(dept=current_employee.dept)
    
    # Exclude the manager themselves from the list
    team_scope = team_scope.exclude(id=current_employee.id)

    # 3. Get Data for Current Period (Example: '1st SEM', '1st' Month)
    # In production, fetch these dynamically based on current date or session filter
    current_year = 2025
    current_sem = "1st SEM"
    current_month = "1st" 

    results = Alk_KPI_Result.objects.filter(
        employee__in=team_scope,
        year=current_year,
        semester=current_sem,
        month=current_month
    ).select_related('employee', 'kpi')

    # 4. Calculate Statistics (The "Big Picture")
    total_staff = team_scope.count()
    
    # Group by Locking Status
    status_counts = results.values('employee').annotate(
        locked_count=Count('id', filter=Q(is_locked=True)),
        total_kpis=Count('id')
    )
    
    # Logic: An employee is "Done" if all their KPIs are locked
    employees_done = 0
    employees_pending = 0
    for s in status_counts:
        if s['locked_count'] == s['total_kpis'] and s['total_kpis'] > 0:
            employees_done += 1
        else:
            employees_pending += 1

    # 5. Anomaly Detection (Outliers)
    # High Alert: Score > 1.2 (Potential input error or exceptional performance)
    # Low Alert: Score < 0.4 (Underperformance)
    anomalies = results.filter(Q(final_result__gt=1.2) | Q(final_result__lt=0.4)).order_by('-final_result')

    context = {
        'stats': {
            'total_staff': total_staff,
            'done': employees_done,
            'pending': employees_pending,
            'completion_rate': round((employees_done / total_staff * 100), 1) if total_staff > 0 else 0
        },
        'anomalies': anomalies[:10], # Top 10 anomalies
        'team_scope': team_scope, # List for the grid
    }
    
    return render(request, 'kpi_app/portal/manager_dashboard.html', context)
B. Frontend Template (manager_dashboard.html)
Layout Structure:

Overview Cards (Top Row):

Card 1 (Blue): Total Staff (e.g., "15 Staff").

Card 2 (Green): Completed/Approved (e.g., "10 Done").

Card 3 (Orange): Pending Review (e.g., "5 Pending").

Card 4 (Purple): Avg Dept Score (e.g., "88%").

Visual Charts (Middle Row):

Left: Pie Chart (Approved vs Pending).

Right: Bar Chart (Score Distribution - How many people are in A, B, C range).

Anomaly Alert Table (Critical Focus):

Header: "⚠️ Attention Needed (Outliers)"

Columns: Employee Name | KPI Name | Target | Achievement | Result | Action.

Purpose: Manager looks here FIRST. If someone entered "10" instead of "0.1", it shows up here immediately as > 140%.

Team Grid (Bottom):

List of all employees.

Status Badge (Done/Pending).

Button: "View Details" (Link to their specific detailed page).

C. Navigation Integration
Update base.html to conditionally show the link.

HTML

{% if user.alk_employee.level <= 1 %}
<li class="nav-item">
    <a class="nav-link fw-bold text-primary" href="{% url 'manager_dashboard' %}">
        <i class="bi bi-speedometer2"></i> Manager Dashboard
    </a>
</li>
{% endif %}
3. Execution Steps for Developer/Agent
Route: Add path('portal/manager/', views.manager_dashboard, name='manager_dashboard') to urls.py.

View: Copy the Python logic above into portal_views.py. Ensure from django.db.models import ... is included.

Template: Create kpi_app/templates/kpi_app/portal/manager_dashboard.html. Use Bootstrap 5 Cards and Grid.

Charts: Include Current version of Chart.js via CDN in the template. Initialize a simple Pie Chart using the data passed from context ({{ stats.done }} vs {{ stats.pending }}).

Testing:

Login as Level 2 -> Try to access /portal/manager/ -> Should redirect or 403.

Login as Level 1 -> Verify statistics match the database.

Create a "Fake" anomaly (Enter a huge number for an employee) -> Verify it appears in the "Attention Needed" table.

4. Why This Works (Business Value)
Focus on Management by Exception: Managers don't need to check 170 people. They only check the "Anomalies" list and the "Pending" list.

Real-time Visibility: "Bức tranh toàn cảnh" helps them push staff to complete KPIs before the deadline (Day 20).

Reduced Error: Visualizing "High Scores" catches the 0.1 vs 10 decimal error immediately.