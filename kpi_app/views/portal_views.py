from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from kpi_app.models import alk_kpi_result, alk_employee
from django.db.models import Count, Avg, Q, Max, Sum

@login_required
def portal_login(request):
    """Custom login view for portal (if needed) or redirect logic."""
    # This might reuse standardized login or provide a specific portal login page
    return redirect('login') 

@login_required
def dashboard(request):
    """Employee Portal Dashboard showing stats and charts."""
    user = request.user
    
    # Access Control: Ensure only appropriate levels access this
    # if user.is_superuser:
    #    return redirect('/admin/')
    
    try:
        employee = alk_employee.objects.get(user_id=user)
    except alk_employee.DoesNotExist:
        messages.error(request, "Employee profile not found.")
        return redirect('logout')

    # Get KPIs for the current active semester/year (Assuming 2025/2nd SEM for now or filtering all)
    # Ideally we'd have a 'current period' setting, but we'll take the latest available year/sem
    latest_year = alk_kpi_result.objects.filter(employee=employee).order_by('-year').values_list('year', flat=True).first()
    
    if not latest_year:
         context = {'page_title': 'Dashboard', 'no_data': True}
         return render(request, 'kpi_app/portal/dashboard.html', context)

    # Filter for latest year
    qs = alk_kpi_result.objects.filter(employee=employee, year=latest_year)
    
    # Stats
    total_kpis = qs.count()
    approved_count = qs.filter(is_locked=True).count()
    pending_count = total_kpis - approved_count
    completion_rate = int((approved_count / total_kpis * 100)) if total_kpis > 0 else 0
    
    # Chart Data: Average Final Result per Month
    from django.db.models import Avg
    monthly_data = qs.values('month').annotate(avg_score=Avg('final_result')).order_by('month')
    
    chart_labels = []
    chart_values = []
    
    # Simple mapping for sorting if needed, or just trust database order
    for item in monthly_data:
        chart_labels.append(item['month'])
        val = item['avg_score'] if item['avg_score'] else 0
        chart_values.append(round(float(val), 2))
        
    context = {
        'page_title': 'Employee Dashboard',
        'user_employee': employee,
        'employee': employee,
        'year': latest_year,
        'completion_rate': completion_rate,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    }
    return render(request, 'kpi_app/portal/dashboard.html', context)

@login_required
def input_form(request):
    """Main data entry grid for employees."""
    user = request.user
    try:
        employee = alk_employee.objects.get(user_id=user)
    except alk_employee.DoesNotExist:
        messages.error(request, "Employee profile not found.")
        return redirect('logout')

    # Get Filter Options
    years = alk_kpi_result.objects.values_list('year', flat=True).distinct().order_by('-year')
    semesters = alk_kpi_result.objects.values_list('semester', flat=True).distinct().order_by('semester')
    months = alk_kpi_result.MONTH_CHOICES

    # Default to current/latest
    current_year = request.GET.get('year') or (years[0] if years else None)
    current_sem = request.GET.get('semester') or (semesters[0] if semesters else None)
    current_month = request.GET.get('month') or (months[0][0] if months else None)

    # Convert to int if possible for Year
    try:
        if current_year: current_year = int(current_year)
    except: pass
    
    kpi_results = alk_kpi_result.objects.filter(employee=employee)
    
    if current_year:
        kpi_results = kpi_results.filter(year=current_year)
    if current_sem:
        kpi_results = kpi_results.filter(semester=current_sem)
    if current_month:
        kpi_results = kpi_results.filter(month=current_month)

    # Ordering
    kpi_results = kpi_results.order_by('kpi__kpi_name')
    
    # Attach Admin Display Formats
    for result in kpi_results:
        _attach_admin_formats(result)

    # Calculate Total Score
    from django.db.models import Sum
    total_val = kpi_results.aggregate(Sum('final_result'))['final_result__sum'] or 0
    total_score = f"{round(total_val * 100, 2):,.2f}%"

    context = {
        'page_title': 'Result Input',
        'user_employee': employee,
        'kpi_results': kpi_results,
        'total_score': total_score,
        'years': years,
        'semesters': semesters,
        'months': months,
        'current_year': current_year,
        'current_sem': current_sem,
        'current_month': current_month,
    }
    return render(request, 'kpi_app/portal/input_form.html', context)

@login_required
def save_kpi_result(request, result_id):
    """HTMX Endpoint to save a single KPI Result."""
    if request.method != "POST":
        return HttpResponse(status=405)
        
    # Get object and ensure it belongs to the user
    result = get_object_or_404(alk_kpi_result, id=result_id, employee__user_id=request.user)
    
    # Permission Check
    if result.is_locked:
         return HttpResponse(
            "<span class='text-danger fw-bold'>Error: Record is Locked. Refresh page.</span>", 
            status=403
        )
    
    warning_msg = None
    
    # --- Handle Achievement Update ---
    # Only allow update if NOT from SAP
    if 'achivement' in request.POST and not result.kpi.from_sap:
        value_str = request.POST.get('achivement')
        try:
            if value_str:
                value_str = value_str.replace(',', '') # Handle commas
                value = float(value_str)
                result.achivement = value
                
                # Smart Validation for Percentage Type
                if result.kpi.kpi_type == 1 and value > 1.5:
                    warning_msg = f"Did you mean {value/100:.2f} ({value}%)? % KPIs should be 0.1 for 10%."
            else:
                result.achivement = None
        except ValueError:
            return HttpResponse("Invalid Number for Achievement", status=400)

    # --- Handle Target Input Update ---
    # Only allow update if percentage_cal is True
    if 'target_input' in request.POST and result.kpi.percentage_cal:
        tgt_str = request.POST.get('target_input')
        try:
            if tgt_str:
                tgt_str = tgt_str.replace(',', '') # Handle commas
                val_tgt = float(tgt_str)
                result.target_input = val_tgt
            else:
                result.target_input = None
        except ValueError:
            return HttpResponse("Invalid Number for Target Input", status=400)

    try:
        result.save() # Triggers calculate_final_result
    except Exception as e:
        return HttpResponse(f"Error saving: {str(e)}", status=500)

    # Apply Admin-like display formatting
    _attach_admin_formats(result)

    # Return the updated row HTML
    return render(request, 'kpi_app/portal/partials/kpi_row.html', {
        'result': result,
        'warning_msg': warning_msg
    })

def _attach_admin_formats(obj):
    """
    Replicates the display logic from AlkKpiResultAdmin to attach formatted strings to the object.
    These attributes are temporary and used for template rendering.
    """
    # 1. Weight: weigth_percent_1f
    if obj.weigth is not None:
        obj.display_weight = f"{round(obj.weigth * 100, 1)}%"
    else:
        obj.display_weight = ""

    # 2. Target Set: target_set_1f
    if obj.target_set is not None:
        if obj.target_set == 0:
             obj.display_target_set = f"{obj.target_set:,.4f}"
        elif obj.kpi and hasattr(obj.kpi, 'percent_display') and obj.kpi.percent_display:
             obj.display_target_set = f"{round(obj.target_set * 100, 3):,.3f}%"
        elif obj.kpi and hasattr(obj.kpi, 'percentage_cal'):
             if obj.kpi.percentage_cal:
                  obj.display_target_set = f"{round(obj.target_set * 100, 3):,.3f}%"
             elif obj.target_set < 1:
                  obj.display_target_set = f"{round(obj.target_set * 100, 3):,.3f}%"
             else:
                  obj.display_target_set = f"{obj.target_set:,.4f}"
        else:
             obj.display_target_set = f"{obj.target_set:,.4f}"
    else:
        obj.display_target_set = ""

    # 3. Target Input: target_input_1f
    if obj.target_input is not None:
        # Prepare Form Value (Comma Separated, Raw Number)
        obj.form_value_target_input = f"{obj.target_input:,.4f}"

        if obj.target_set == 0:
             obj.display_target_input = f"{obj.target_input:,.4f}"
        elif obj.kpi and hasattr(obj.kpi, 'percent_display') and obj.kpi.percent_display:
             obj.display_target_input = f"{round(obj.target_input * 100, 3):,.3f}%"
        elif obj.kpi and hasattr(obj.kpi, 'percentage_cal') and obj.kpi.percentage_cal:
             obj.display_target_input = f"{round(obj.target_input * 100, 3):,.3f}%"
        elif obj.kpi and hasattr(obj.kpi, 'percentage_cal') and obj.kpi.percentage_cal is False and obj.target_set is not None and obj.target_set < 1:
             obj.display_target_input = f"{round(obj.target_input * 100, 3):,.3f}%"
        else:
             obj.display_target_input = f"{obj.target_input:,.4f}"
    else:
        obj.display_target_input = ""
        obj.form_value_target_input = ""

    # 4. Achievement: achivement_1f
    if obj.achivement is not None:
        # Prepare Form Value (Comma Separated, Raw Number)
        obj.form_value_achivement = f"{obj.achivement:,.4f}"

        if obj.target_set == 0:
             obj.display_achivement = f"{obj.achivement:,.4f}"
        elif obj.kpi and hasattr(obj.kpi, 'percent_display') and obj.kpi.percent_display:
             obj.display_achivement = f"{round(obj.achivement * 100, 3):,.3f}%"
        elif obj.kpi and hasattr(obj.kpi, 'percentage_cal') and obj.kpi.percentage_cal:
             obj.display_achivement = f"{round(obj.achivement * 100, 3):,.3f}%"
        elif obj.kpi and hasattr(obj.kpi, 'percentage_cal') and obj.kpi.percentage_cal is False and obj.target_set is not None and obj.target_set < 1:
             obj.display_achivement = f"{round(obj.achivement * 100, 3):,.3f}%"
        else:
             obj.display_achivement = f"{obj.achivement:,.4f}"
    else:
        obj.display_achivement = ""
        obj.form_value_achivement = ""

    # 5. Final Result: final_result_percent_1f
    if obj.final_result is not None:
        obj.display_final_result = f"{round(obj.final_result * 100, 1)}%"
    else:
        obj.display_final_result = ""

@login_required
def manager_dashboard(request):
    """
    Command Center for Level 1 (Dept Manager) and Level 0 (Group Manager).
    """
    user = request.user
    
    try:
        current_employee = alk_employee.objects.get(user_id=user)
    except alk_employee.DoesNotExist:
        return redirect('portal_dashboard')

    # 1. Security Check
    if current_employee.level > 1:
        # Unauthorized for dashboard, redirect to personal portal
        return redirect('portal_dashboard')

    # 2. Scope Definition
    if current_employee.level == 0:
        # Group Manager: Filter by Dept Group based on string match in Dept Table
        # Logic: All employees whose Department belongs to the same Group Name as the Manager's Department
        my_group_name = current_employee.dept.group
        team_scope = alk_employee.objects.filter(dept__group=my_group_name)
    else:
        # Dept Manager (Level 1): Filter by Department
        team_scope = alk_employee.objects.filter(dept=current_employee.dept)
    
    # Exclude manager themselves from the stats
    team_scope_ids = team_scope.exclude(id=current_employee.id).values_list('id', flat=True)

    # 3. Data Fetching - Filter Logic
    # Get available filter choices from database (distinct values)
    available_years = alk_kpi_result.objects.filter(
        employee__id__in=team_scope_ids
    ).values_list('year', flat=True).distinct().order_by('-year')
    
    available_semesters = alk_kpi_result.objects.filter(
        employee__id__in=team_scope_ids
    ).values_list('semester', flat=True).distinct().order_by('semester')
    
    available_months = alk_kpi_result.objects.filter(
        employee__id__in=team_scope_ids
    ).values_list('month', flat=True).distinct().order_by('month')
    
    # Convert to lists and ensure we have data
    year_choices = list(available_years) if available_years else [2025]
    sem_choices = list(available_semesters) if available_semesters else ['1st SEM', '2nd SEM']
    month_choices = list(available_months) if available_months else ['1st', '2nd', '3rd', '4th', '5th', '6th']
    
    selected_year = request.GET.get('year', 'All')
    selected_sem = request.GET.get('semester', 'All')
    selected_month = request.GET.get('month', 'All')

    # Build query filters dynamically
    filter_kwargs = {'employee__id__in': team_scope_ids}
    
    if selected_year != 'All':
        filter_kwargs['year'] = int(selected_year)
    
    if selected_sem != 'All':
        filter_kwargs['semester'] = selected_sem
    
    if selected_month != 'All':
        filter_kwargs['month'] = selected_month

    results = alk_kpi_result.objects.filter(**filter_kwargs).select_related('employee', 'kpi')

    # 4. Aggregation
    total_staff = team_scope.count() - 1 # Subtract manager if they were in the count, basically usage of exclude above handles it
    if total_staff < 0: total_staff = 0 # Safety

    # Calculate Status (Employee Level)
    # An employee is "Done" if ALL their KPIs for the FILTERED period are locked
    # This works correctly whether filtering by specific period or "All"
    emp_stats = results.values('employee').annotate(
        total_kpis=Count('id'),
        locked_kpis=Count('id', filter=Q(is_locked=True))
    )
    
    done_count = 0
    employees_with_kpis = set()
    
    for s in emp_stats:
        employees_with_kpis.add(s['employee'])
        if s['total_kpis'] > 0 and s['total_kpis'] == s['locked_kpis']:
            done_count += 1
    
    # Pending = employees with KPIs that are not all locked
    pending_count = len(employees_with_kpis) - done_count

    avg_score = results.aggregate(Avg('final_result'))['final_result__avg'] or 0

    # 5. Anomalies
    # > 1.2 (120%) or < 0.4 (40%)
    anomalies = results.filter(
        Q(final_result__gt=1.2) | Q(final_result__lt=0.4)
    ).order_by('-final_result')[:10] # Top 10

    # Format anomalies for display
    for a in anomalies:
        _attach_admin_formats(a)

    context = {
        'page_title': 'Manager Dashboard',
        'user_employee': current_employee,
        'stats': {
            'total_staff': total_staff,
            'done': done_count,
            'pending': pending_count,
            'avg_score': f"{round(avg_score * 100, 1)}%",
            'completion_rate': round((done_count / total_staff * 100), 1) if total_staff > 0 else 0
        },
        'anomalies': anomalies,
        'filters': {
            'year': selected_year,
            'semester': selected_sem,
            'month': selected_month,
            'year_options': [
                {'value': 'All', 'label': 'All Years', 'selected': selected_year == 'All'},
            ] + [{'value': y, 'label': str(y), 'selected': str(selected_year) == str(y)} for y in year_choices],
            'sem_options': [
                {'value': 'All', 'label': 'All Semesters', 'selected': selected_sem == 'All'},
            ] + [{'value': s, 'label': s, 'selected': selected_sem == s} for s in sem_choices],
            'month_options': [
                {'value': 'All', 'label': 'All Months', 'selected': selected_month == 'All'},
            ] + [{'value': m, 'label': f'{m} Month', 'selected': selected_month == m} for m in month_choices],
        }
    }

    return render(request, 'kpi_app/portal/manager_dashboard.html', context)

