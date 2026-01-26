import os

file_path = r"C:\dev\alkana_kpi\kpi_app\templates\kpi_app\portal\input_form.html"

content = """{% extends 'kpi_app/portal/base.html' %}

{% block content %}
<div class="row mb-4 fade-in-up">
    <div class="col-12 text-center text-md-start">
        <h2 class="fw-bold mb-1">Data Entry</h2>
        <p class="text-secondary">Update your KPI achievements for the selected period.</p>
    </div>
</div>

<!-- Filters -->
<div class="row mb-4">
    <div class="col-12">
        <div class="glass-card p-4">
            <form method="get" class="row g-3 align-items-end">
                <div class="col-md-3">
                    <label class="form-label fw-bold small text-uppercase">Year</label>
                    <select name="year" class="form-select input-glass" onchange="this.form.submit()">
                        {% for y in years %}
                        <option value="{{ y }}" {% if y == current_year %}selected{% endif %}>{{ y }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label class="form-label fw-bold small text-uppercase">Semester</label>
                    <select name="semester" class="form-select input-glass" onchange="this.form.submit()">
                        {% for s in semesters %}
                        <option value="{{ s }}" {% if s == current_sem %}selected{% endif %}>{{ s }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label class="form-label fw-bold small text-uppercase">Month</label>
                    <select name="month" class="form-select input-glass" onchange="this.form.submit()">
                        {% for m_code, m_name in months %}
                        <option value="{{ m_code }}" {% if m_code == current_month %}selected{% endif %}>{{ m_name }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3 text-end">
                    <a href="{% url 'portal_dashboard' %}" class="btn btn-outline-secondary rounded-pill px-4">
                        <i class="bi bi-arrow-left me-2"></i> Back
                    </a>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Data Table -->
<div class="row">
    <div class="col-12">
        <div class="glass-card overflow-hidden">
            <div class="table-responsive">
                <table class="table table-glass align-middle">
                    <thead>
                        <tr>
                            <th class="ps-4" style="width: 25%;">KPI Name</th>
                            <th>Weight</th>
                            <th>Target Set</th>
                            <th style="width: 15%;">Target Input</th>
                            <th style="width: 15%;">Achievement</th>
                            <th>Score</th>
                            <th class="text-end pe-4">Status</th>
                        </tr>
                    </thead>
                    <tbody id="kpi-table-body">
                        {% for result in kpi_results %}
                        {% include 'kpi_app/portal/partials/kpi_row.html' with result=result %}
                        {% empty %}
                        <tr>
                            <td colspan="7" class="text-center py-5 text-muted">
                                <i class="bi bi-inbox fs-1 d-block mb-3 opacity-50"></i>
                                No KPIs found for this selection.
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

try:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"SUCCESS: Written to {file_path}")
    
    # Read back to verify
    with open(file_path, 'r', encoding='utf-8') as f:
        read_content = f.read()
        if "{% if y == current_year %}" in read_content:
            print("VERIFICATION: Syntax check PASSED.")
        else:
            print("VERIFICATION: Syntax check FAILED.")
            
        if "Target Input" in read_content:
             print("VERIFICATION: Header check PASSED.")
        else:
             print("VERIFICATION: Header check FAILED.")

except Exception as e:
    print(f"ERROR: {e}")
