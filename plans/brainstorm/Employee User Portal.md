# Phase 2: Implementation Plan - Employee User Portal
**Project:** Alkana KPI System
**Objective:** Decouple End Users (Level 2) from the Django Admin interface by creating a dedicated, user-friendly "Employee Portal" using Bootstrap 5 and HTMX.
**Key Features:** Custom Dashboard, "Smart" Input Forms (Validation), Visual Status Feedback (Approved/Pending).

---

## 1. Technical Stack & Dependencies

To ensure a modern, responsive UI without heavy frontend frameworks (React/Vue), we will use:
* **CSS Framework:** Bootstrap 5.3 (via CDN or Static).
* **Interactivity:** HTMX (via CDN or Static) for AJAX requests and smooth updates.
* **Charts:** Chart.js (for the Dashboard).
* **Backend:** Django (Standard Views + Templates).

---

## 2. Directory Structure Changes

Refactor `kpi_app` to separate Admin logic from Portal logic.

```text
kpi_app/
├── views/                  <-- Refactor views.py into a package
│   ├── __init__.py
│   ├── admin_views.py      # Existing admin-related views (if any)
│   └── portal_views.py     # NEW: Logic for the Employee Portal
├── urls.py                 # Main app URLs
├── templates/
│   └── kpi_app/
│       ├── portal/         # NEW: Templates for the portal
│       │   ├── base.html
│       │   ├── login.html
│       │   ├── dashboard.html
│       │   └── partials/   # HTMX partials
│       │       └── kpi_row.html
3. URL Routing Strategy
File: kpi_app/urls.py

Define a dedicated namespace for the portal.

Python

from django.urls import path
from .views import portal_views

urlpatterns = [
    # ... existing admin/api urls ...

    # PORTAL URLS
    path('portal/login/', portal_views.portal_login, name='portal_login'),
    path('portal/logout/', portal_views.portal_logout, name='portal_logout'),
    path('portal/', portal_views.dashboard, name='portal_dashboard'),
    path('portal/input/<int:year>/<str:semester>/<str:month>/', portal_views.input_form, name='portal_input'),
    
    # HTMX Endpoints
    path('portal/save-kpi/<int:result_id>/', portal_views.save_kpi_result, name='portal_save_kpi'),
]
4. Implementation Details
A. Custom Login & Redirection
Logic: Intercept the login flow.

If User is Superuser or Level 0/1: Redirect to /admin/ (or give choice).

If User is Level 2: Redirect strictly to /portal/.

B. Dashboard View (portal_views.dashboard)
Objective: Show summary statistics.

Data: Calculate % Completion of current month.

Visuals: Render a Bar Chart using Chart.js showing scores for the last 6 months.

Status: Show a big Badge: "Pending" (Grey) or "Approved" (Green) for the current month.

C. Input Form View (portal_views.input_form)
Objective: Replace the Admin Grid.

Validation Logic (The "0.1 vs 10" Fix): We will implement a "Smart Save" using HTMX.

Python

# portal_views.py (Pseudo-code)

@login_required
def save_kpi_result(request, result_id):
    result = get_object_or_404(Alk_KPI_Result, id=result_id, employee__user=request.user)
    
    # Security Check: Approved/Locked
    if result.is_locked:
        return HttpResponse("Error: Record is Approved and Locked.", status=403)

    value = request.POST.get('achievement')
    
    # VALIDATION LOGIC
    # Check if KPI is Type 1 (Percentage based)
    if result.kpi.kpi_type == 1: 
        try:
            float_val = float(value)
            # Threshold Check: If user types "10" (1000%) instead of "0.1" (10%)
            if float_val > 1.5: 
                return HttpResponse(
                    f"<span class='text-danger'>Suspicious value ({float_val}). Did you mean {float_val/100}?</span>", 
                    status=400
                )
        except ValueError:
            pass

    # Save logic...
    result.achievement = value
    result.save() # Recalculates final_result
    
    # Return updated row HTML
    return render(request, 'kpi_app/portal/partials/kpi_row.html', {'result': result})
D. Frontend Interface (Bootstrap 5)
Template: kpi_app/portal/partials/kpi_row.html This represents a single row in the input table.

HTML

<tr class="{% if result.is_locked %}table-success{% endif %}">
    <td>{{ result.kpi.kpi_name }}</td>
    <td>{{ result.target_set }}</td>
    
    <td>
        {% if result.is_locked %}
            <span class="fw-bold text-success">{{ result.achievement }}</span>
            <i class="bi bi-check-circle-fill text-success" title="Approved"></i>
        {% else %}
            <input type="number" 
                   step="0.0001" 
                   class="form-control" 
                   name="achievement" 
                   value="{{ result.achievement }}"
                   hx-post="{% url 'portal_save_kpi' result.id %}"
                   hx-trigger="change delay:500ms"
                   hx-target="closest tr"
                   hx-swap="outerHTML">
        {% endif %}
    </td>
    
    <td>{{ result.final_result }}</td>
</tr>
5. Security & Access Control Guidelines
Row-Level Security: Every view MUST filter by request.user.

Python

# BAD
Alk_KPI_Result.objects.all()

# GOOD
Alk_KPI_Result.objects.filter(employee__user=request.user)
Hard Lock Check: The save_kpi_result view must explicitly check if result.is_locked: before saving, even if the UI is hidden (to prevent API manipulation).

6. Execution Steps for Developer/Agent
Setup: Create the templates/kpi_app/portal directory and add Bootstrap 5/HTMX CDNs to base.html.

Auth: Create the portal_login view and template. Ensure redirection logic works based on Employee Level.

Dashboard: Build the dashboard view to fetch the current user's data and render dashboard.html.

Input: Implement the input_form view and the kpi_row.html partial.

Validation: Implement the backend validation logic for "Percentage vs Absolute" values inside the save view.

Testing:

Log in as Level 2 -> Verify redirection to Portal.

Try to edit an "Approved" (is_locked=True) record -> Should be impossible UI/Backend.

Input "10" for a percentage KPI -> Verify warning message.