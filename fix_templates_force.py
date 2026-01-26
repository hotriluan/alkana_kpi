import os

BASE_DIR = os.getcwd()

input_form_path = os.path.join(BASE_DIR, 'kpi_app', 'templates', 'kpi_app', 'portal', 'input_form.html')
dashboard_path = os.path.join(BASE_DIR, 'kpi_app', 'templates', 'kpi_app', 'portal', 'dashboard.html')

input_form_content = """{% extends 'kpi_app/portal/base.html' %}

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
                            <th>Target</th>
                            <th style="width: 20%;">Achievement</th>
                            <th>Score</th>
                            <th class="text-end pe-4">Status</th>
                        </tr>
                    </thead>
                    <tbody id="kpi-table-body">
                        {% for result in kpi_results %}
                        {% include 'kpi_app/portal/partials/kpi_row.html' with result=result %}
                        {% empty %}
                        <tr>
                            <td colspan="6" class="text-center py-5 text-muted">
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

dashboard_content = """{% extends 'kpi_app/portal/base.html' %}
{% load static %}

{% block content %}
<div class="row mb-5 fade-in-up">
    <div class="col-12">
        <div class="glass-card p-5 text-center text-md-start d-flex flex-column flex-md-row align-items-center justify-content-between position-relative overflow-hidden">
            <!-- Decorative Background Blob -->
            <div class="position-absolute top-0 end-0 p-5 rounded-circle bg-primary opacity-10"
                style="margin-top: -50px; margin-right: -50px; width: 200px; height: 200px; filter: blur(60px);"></div>

            <div class="z-1">
                <h1 class="display-5 fw-bold mb-2">Welcome back, <span class="text-primary-gradient">{{ employee.name }}</span>!</h1>
                <p class="text-secondary lead mb-0">{{ employee.job_title.title_name }} | {{ employee.dept.dept_name }}</p>
                <p class="text-muted small mt-2"><i class="bi bi-calendar-check me-1"></i> Data for Year: <strong>{{ year }}</strong></p>
            </div>

            <div class="mt-4 mt-md-0 z-1 text-center">
                <div class="d-inline-flex align-items-center justify-content-center position-relative">
                    <svg viewBox="0 0 36 36" class="circular-chart text-primary" style="width: 120px; height: 120px;">
                        <path class="circle-bg"
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none" stroke="#eee" stroke-width="3" />
                        <path class="circle" stroke-dasharray="{{ completion_rate }}, 100"
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none" stroke="#667eea" stroke-width="3" stroke-linecap="round" />
                    </svg>
                    <div class="position-absolute top-50 start-50 translate-middle">
                        <span class="h3 fw-bold m-0">{{ completion_rate }}%</span>
                        <div class="small text-muted">Complete</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row g-4 mb-5">
    <!-- Pending Card -->
    <div class="col-md-4">
        <div class="glass-card p-4 h-100 d-flex align-items-center justify-content-between">
            <div>
                <p class="text-secondary mb-1 fw-bold text-uppercase small">Pending Review</p>
                <h2 class="display-6 fw-bold text-warning mb-0">{{ pending_count }}</h2>
            </div>
            <div class="bg-warning-subtle text-warning rounded-circle p-3">
                <i class="bi bi-hourglass-split fs-3"></i>
            </div>
        </div>
    </div>

    <!-- Approved Card -->
    <div class="col-md-4">
        <div class="glass-card p-4 h-100 d-flex align-items-center justify-content-between">
            <div>
                <p class="text-secondary mb-1 fw-bold text-uppercase small">Approved KPIs</p>
                <h2 class="display-6 fw-bold text-success mb-0">{{ approved_count }}</h2>
            </div>
            <div class="bg-success-subtle text-success rounded-circle p-3">
                <i class="bi bi-check-lg fs-3"></i>
            </div>
        </div>
    </div>

    <!-- Action Card -->
    <div class="col-md-4">
        <div class="glass-card p-4 h-100 d-flex flex-column justify-content-center align-items-start">
            <h5 class="fw-bold mb-2">Need to update?</h5>
            <p class="text-secondary small mb-3">Keep your KPIs up to date for accurate reporting.</p>
            <a href="{% url 'portal_input' %}" class="btn btn-primary-gradient w-100 rounded-pill fw-bold">
                Go to Data Entry <i class="bi bi-arrow-right ms-2"></i>
            </a>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="glass-card p-4">
            <div class="d-flex align-items-center justify-content-between mb-4">
                <h5 class="fw-bold m-0"><i class="bi bi-graph-up-arrow me-2 text-primary"></i>Performance Trend</h5>
                <span class="badge bg-primary-subtle text-primary">Monthly Average</span>
            </div>
            <div style="height: 350px;">
                <canvas id="performanceChart"></canvas>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
{{ chart_labels|json_script:"chart-labels-data" }}
{{ chart_values|json_script:"chart-values-data" }}
<script>
    document.addEventListener('DOMContentLoaded', function () {
        const ctx = document.getElementById('performanceChart').getContext('2d');

        // Data from Django - using json_script for safety
        const labels = JSON.parse(document.getElementById('chart-labels-data').textContent);
        const data = JSON.parse(document.getElementById('chart-values-data').textContent);

        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(102, 126, 234, 0.5)');
        gradient.addColorStop(1, 'rgba(102, 126, 234, 0.0)');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Average Score',
                    data: data,
                    borderColor: '#667eea',
                    backgroundColor: gradient,
                    borderWidth: 3,
                    pointBackgroundColor: '#fff',
                    pointBorderColor: '#764ba2',
                    pointHoverBackgroundColor: '#764ba2',
                    pointHoverBorderColor: '#fff',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        titleColor: '#2d3748',
                        bodyColor: '#2d3748',
                        borderColor: 'rgba(0,0,0,0.1)',
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)',
                            borderDash: [5, 5]
                        },
                        ticks: {
                            font: { family: 'Inter' }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: { family: 'Inter' }
                        }
                    }
                }
            }
        });
    });
</script>
{% endblock %}
"""

with open(input_form_path, 'w', encoding='utf-8') as f:
    f.write(input_form_content)
    print(f"Successfully wrote {input_form_path}")

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(dashboard_content)
    print(f"Successfully wrote {dashboard_path}")
