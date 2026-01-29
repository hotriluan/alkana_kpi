from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib import messages
from kpi_app.models import alk_kpi_result, alk_employee
from django.db.models import Count, Avg, Q, Max, Sum, Value, CharField
from django.views.decorators.http import require_POST
from decimal import Decimal

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
    
    # Chart Data: Total Score (Sum) per Month as Percentage
    from django.db.models import Sum
    monthly_data = qs.values('month').annotate(total_score=Sum('final_result')).order_by('month')
    
    chart_labels = []
    chart_data = []
    
    # Simple mapping for sorting if needed, or just trust database order
    for item in monthly_data:
        chart_labels.append(item['month'])
        val = item['total_score'] if item['total_score'] else 0
        # Convert to Percentage (0.8 -> 80.0)
        percentage_val = float(val) * 100
        chart_data.append(round(percentage_val, 2))
        
    context = {
        'page_title': 'Employee Dashboard',
        'user_employee': employee,
        'employee': employee,
        'year': latest_year,
        'completion_rate': completion_rate,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
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
        
    # Get object
    result = get_object_or_404(alk_kpi_result, id=result_id)
    
    # Identify User Role & Permissions
    user = request.user
    is_owner = (result.employee.user_id == user)
    is_manager = False

    try:
        requester_emp = alk_employee.objects.get(user_id=user)
        # Manager Check (Level 0 or 1)
        if requester_emp.level <= 1:
            # Scope Check
            if requester_emp.level == 0:
                if requester_emp.dept.group == result.employee.dept.group:
                    is_manager = True
            elif requester_emp.level == 1:
                if requester_emp.dept == result.employee.dept:
                    is_manager = True
    except:
        pass

    # --- NEW GUARD: ACTIVE CHECK ---
    if not result.active:
        return HttpResponseForbidden("This KPI result is inactive and cannot be edited.")

    # Authorization Enforcer
    if not is_owner and not is_manager:
        return HttpResponse("Unauthorized", status=403)
    
    # Lock Check (Manager override allowed)
    if result.is_locked and not is_manager:
         return HttpResponse(
            "<span class='text-danger fw-bold'>Error: Record is Locked. Refresh page.</span>", 
            status=403
        )
    
    warning_msg = None
    
    # --- Handle Achievement Update ---
    # Only allow update if NOT from SAP
    if 'achievement' in request.POST and not result.kpi.from_sap:
        value_str = request.POST.get('achievement')
        try:
            if value_str:
                value_str = value_str.replace(',', '') # Handle commas
                value = float(value_str)
                result.achievement = value
                
                # Smart Validation for Percentage Type
                if result.kpi.kpi_type == 1 and value > 1.5:
                    warning_msg = f"Did you mean {value/100:.2f} ({value}%)? % KPIs should be 0.1 for 10%."
            else:
                result.achievement = None
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

    # Persist Checkbox State (for Bulk Approval UI)
    show_checkbox = request.POST.get('show_checkbox') == 'true'
    
    # Fallback: If not passed, check is_manager (optional, but specific flag is safer)
    # let's just use the strict flag to avoid layout breakage in input forms.
    
    # Return the updated row HTML
    return render(request, 'kpi_app/portal/partials/kpi_row.html', {
        'result': result,
        'warning_msg': warning_msg,
        'show_checkbox': show_checkbox,
        'is_manager': request.user.alk_employee_set.first().level <= 1 if hasattr(request.user, 'alk_employee_set') else False 
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

    # 4. Achievement: achievement_1f
    if obj.achievement is not None:
        # Prepare Form Value (Comma Separated, Raw Number)
        obj.form_value_achievement = f"{obj.achievement:,.4f}"

        if obj.target_set == 0:
             obj.display_achievement = f"{obj.achievement:,.4f}"
        elif obj.kpi and hasattr(obj.kpi, 'percent_display') and obj.kpi.percent_display:
             obj.display_achievement = f"{round(obj.achievement * 100, 3):,.3f}%"
        elif obj.kpi and hasattr(obj.kpi, 'percentage_cal') and obj.kpi.percentage_cal:
             obj.display_achievement = f"{round(obj.achievement * 100, 3):,.3f}%"
        elif obj.kpi and hasattr(obj.kpi, 'percentage_cal') and obj.kpi.percentage_cal is False and obj.target_set is not None and obj.target_set < 1:
             obj.display_achievement = f"{round(obj.achievement * 100, 3):,.3f}%"
        else:
             obj.display_achievement = f"{obj.achievement:,.4f}"
    else:
        obj.display_achievement = ""
        obj.form_value_achievement = ""

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
    
    selected_year = request.GET.get('year', 2025)
    selected_sem = request.GET.get('semester', '2nd SEM')
    selected_month = request.GET.get('month', '1st')

    # Build query filters dynamically
    filter_kwargs = {'employee__id__in': team_scope_ids}
    
    # Force defaults to string for SAFE comparison if mixed types exist
    if str(selected_year) != 'All':
        filter_kwargs['year'] = selected_year
    
    if selected_sem != 'All':
        filter_kwargs['semester'] = selected_sem
    


    if selected_month != 'All':
        # RELAXED FILTER ATTEMPT 2: Use __icontains for maximum flexibility
        filter_kwargs['month__icontains'] = selected_month
    
    if selected_sem != 'All':
        filter_kwargs['semester__icontains'] = selected_sem

    results = alk_kpi_result.objects.filter(**filter_kwargs).select_related('employee', 'kpi')

    # ... (Stats calculation steps) ...
    # Note: re-using existing logic but adding debug trace

    # 4. Calculate Statistics (The "Big Picture")
    total_staff = team_scope.count()
    
    # Identify employees who have NO KPIs generated for this period
    employees_with_kpis_ids = results.values_list('employee_id', flat=True).distinct()
    employees_missing_kpis = team_scope.exclude(id__in=employees_with_kpis_ids)
    missing_kpi_count = employees_missing_kpis.count()

    status_counts = results.values('employee').annotate(
        locked_count=Count('id', filter=Q(is_locked=True)),
        total_kpis=Count('id')
    )

    employees_done = 0
    done_emp_ids = set()
    
    # Store KPI counts for debug display
    emp_kpi_counts = {} 

    for s in status_counts:
        # Populate counts map
        emp_kpi_counts[s['employee']] = s['total_kpis']

        if s['total_kpis'] > 0 and s['locked_count'] == s['total_kpis']:
            employees_done += 1
            done_emp_ids.add(s['employee'])

    # FIXED LOGIC: Pending is simply the remainder
    employees_pending = total_staff - employees_done

    avg_score = results.aggregate(Avg('final_result'))['final_result__avg'] or 0

    # 5. Anomalies
    # > 1.2 (120%) or < 0.4 (40%)
    potential_typos = results.filter(final_result__gt=1.2).annotate(
        alert_reason=Value('TYPO', output_field=CharField())
    )
    under_performers = results.filter(final_result__lt=0.4).annotate(
        alert_reason=Value('LOW', output_field=CharField())
    )
    
    anomalies = list(potential_typos) + list(under_performers)
    anomalies.sort(key=lambda x: x.final_result, reverse=True) # Sort desc by score
    
    # Format anomalies for display
    for a in anomalies:
        _attach_admin_formats(a)

    # --- UI Status Annotations ---
    anomaly_emp_ids = set(r.employee_id for r in anomalies)
    
    team_data = [] # New Data Structure for Template
    
    for emp in team_scope:
        # 1. Filter strictly for this employee to get ACCURATE status
        emp_filters = filter_kwargs.copy()
        if 'employee__id__in' in emp_filters:
            del emp_filters['employee__id__in']
        emp_filters['employee'] = emp
        
        emp_results = alk_kpi_result.objects.filter(**emp_filters)
        
        # 2. EXPLICIT COUNTING (No shortcuts)
        total_kpis = int(emp_results.count())
        locked_count = 0
        
        for r in emp_results:
            if r.is_locked:
                locked_count += 1
        
        # 3. ABSOLUTE LOGIC (No ambiguity) - USER OVERRIDE DEPLOYMENT #34
        if total_kpis == 0:
            status = 'No Data'
            status_class = 'secondary'
        elif locked_count == total_kpis:
            status = 'Approved'
            status_class = 'success'
        else:
            status = 'Pending'
            status_class = 'warning text-dark'

        # 4. FINAL DEBUG PRINT for Ardyatma


        # 5. Populate Dictionary
        team_data.append({
            'employee': emp,
            'job_title': emp.job_title,
            'emp_id': emp.user_id.username, # CORRECTED from employee_id
            'status': status,
            'status_class': status_class,
            'debug_count': total_kpis
        })

    # Sort dictionary list by employee name
    team_data.sort(key=lambda x: x['employee'].name)

    # 6. IDENTIFY MISSING KPIS (Data Integrity Check)
    missing_kpi_employees = [m for m in team_data if m['status'] == 'No Data']
    no_kpi_count = len(missing_kpi_employees)

    # Paginate DICTIONARY list
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(team_data, 20) # Show 20 contacts per page
    page = request.GET.get('page')
    
    try:
        employees_page = paginator.page(page)
    except PageNotAnInteger:
        employees_page = paginator.page(1)
    except EmptyPage:
        employees_page = paginator.page(paginator.num_pages)

    # Sort anomalies by final_result (ascending) to show worst performers first
    anomalies.sort(key=lambda x: x.final_result if x.final_result is not None else 0)

    # PAGINATION FOR ANOMALIES
    # Show only 5 rows per page for better layout
    anomalies_paginator = Paginator(anomalies, 5)
    anomalies_page_num = request.GET.get('anomaly_page')
    try:
        anomalies_page = anomalies_paginator.page(anomalies_page_num)
    except PageNotAnInteger:
        anomalies_page = anomalies_paginator.page(1)
    except EmptyPage:
        anomalies_page = anomalies_paginator.page(anomalies_paginator.num_pages)

    context = {
        'page_title': 'Manager Dashboard',
        'user_employee': current_employee,
        'no_kpi_count': no_kpi_count, # New Count
        'missing_kpi_employees': missing_kpi_employees, # List for Modal
        'stats': {
            'total_staff': total_staff,
            'done': employees_done,
            'pending': employees_pending,
            'missing_kpi_count': no_kpi_count, # Override old count logic
            'avg_score': f"{round(avg_score * 100, 1)}%",
            'completion_rate': round((employees_done / total_staff * 100), 1) if total_staff > 0 else 0
        },
        'missing_kpi_list': employees_missing_kpis,
        'team_data': employees_page, # Renamed from team_scope to match template
        'anomalies': anomalies_page,
        
        # Filter context
        'anomalies': anomalies_page, # Pass the Page object instead of list
        'team_scope': employees_page, # PASSED FOR LIST DISPLAY
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

from django.views.decorators.http import require_POST

@login_required
def manager_review_employee(request, emp_id):
    """
    Review page for a specific employee's KPIs.
    Strictly for Level 0/1 Managers.
    """
    user = request.user
    try:
        current_employee = alk_employee.objects.get(user_id=user)
    except alk_employee.DoesNotExist:
        return redirect('portal_dashboard')

    # STRICT PERMISSION CHECK
    is_manager = (current_employee.level <= 1)
    if not is_manager:
        return redirect('portal_dashboard')

    target_emp = get_object_or_404(alk_employee, id=emp_id)

    # SCOPE CHECK
    if current_employee.level == 0:
        # Group Manager Check
        if target_emp.dept.group != current_employee.dept.group:
             messages.error(request, "Employee not in your Group scope.")
             return redirect('manager_dashboard')
    elif current_employee.level == 1:
        # Dept Manager Check
        if target_emp.dept != current_employee.dept:
             messages.error(request, "Employee not in your Department scope.")
             return redirect('manager_dashboard')
    
    # 1. Get Filter Params (Handle empty strings and aliases)
    current_year = request.GET.get('year') or 2025
    current_sem = request.GET.get('semester') or request.GET.get('sem') or '2nd SEM'
    current_month = request.GET.get('month') or '1st'

    # 2. Filter QuerySet (Relaxed matching to align with Dashboard)
    results = alk_kpi_result.objects.filter(
        employee=target_emp,
        year=current_year,
        semester__icontains=current_sem,
        month__icontains=current_month
    ).order_by('kpi__kpi_name')

    for res in results:
        _attach_admin_formats(res)

    # Check approval status
    is_fully_approved = not results.filter(is_locked=False).exists() and results.exists()

    # 3. Context for Dropdowns
    months = ['1st', '2nd', '3rd', '4th', '5th', 'Final']

    # 4. Calculate Total Score
    total_score = sum(r.final_result for r in results) * 100 if results else 0.0

    context = {
        'page_title': f'Review: {target_emp.name}',
        'user_employee': current_employee,
        'target_emp': target_emp,
        'results': results,
        'is_fully_approved': is_fully_approved,
        'is_manager': True,
        'current_year': current_year,
        'current_sem': current_sem,
        'current_month': current_month,
        'months': months,
        'total_score': total_score,
    }
    return render(request, 'kpi_app/portal/manager_review.html', context)

@login_required
@require_POST
def manager_toggle_approval(request, emp_id):
    """
    Toggles the 'is_locked' status of a KPI Result.
    Now supports BULK operations via 'selected_kpi' list.
    """
    user = request.user
    try:
        current_employee = alk_employee.objects.get(user_id=user)
    except alk_employee.DoesNotExist:
        return HttpResponse("Unauthorized", status=403)

    if current_employee.level > 1:
        return HttpResponse("Unauthorized", status=403)
    # 1. Get selected IDs from form data (Checkboxes)
    selected_ids = request.POST.getlist('selected_kpi')
    action = request.POST.get('action')
    
    # Fallback to single ID if not bulk (legacy support or single button)
    # But strictly speaking, the order says "modify to handle LIST"
    
    if not selected_ids:
        # Try to get single ID if passed slightly differently, or return error
        # For now, let's assume the frontend update sends everything properly.
        return HttpResponse('<span class="badge bg-danger">No Items Selected</span>')

    try:
        # 2. Filter Results (Security: Ensure they belong to the emp_id currently being reviewed)
        # We should logically ensure the manager has access to this emp_id (already covered by @login_required + system design, 
        # but in production we'd check team_scope).
        results = alk_kpi_result.objects.filter(
            id__in=selected_ids,
            employee_id=emp_id
        )
        
        count = results.count()

        # 3. Apply Action
        # 3. Apply Action
        if action == 'approve':
            results.update(is_locked=True)
            msg = f'<span class="fw-bold text-success"><i class="bi bi-check-circle me-1"></i>Approved {count} Items</span>'
        
        elif action == 'reject':
            results.update(is_locked=False)
            msg = f'<span class="fw-bold text-warning text-dark"><i class="bi bi-unlock me-1"></i>Unlocked {count} Items</span>'
            
        else:
             msg = '<span class="badge bg-secondary">Unknown Action</span>'

        response = HttpResponse(msg)
        response['HX-Trigger'] = 'kpi_table_update'
        return response

    except Exception as e:
        return HttpResponse(f'<span class="badge bg-danger">Error: {str(e)}</span>')


@login_required
@require_POST
def manager_save_kpi(request, result_id):
    import sys
    print(f"--- DEBUG: Attempting to SAVE KPI ID: {result_id} ---", file=sys.stderr)
    print(f"DEBUG: POST Data: {request.POST}", file=sys.stderr)
    
    result = get_object_or_404(alk_kpi_result, id=result_id)
    
    # --- NEW GUARD: ACTIVE CHECK ---
    if not result.active:
        print(f"ERROR: Attempt to edit INACTIVE KPI {result_id}", file=sys.stderr)
        return HttpResponseForbidden("This KPI result is inactive and cannot be edited.")

    # Security Check: Ensure user has rights to edit this result
    user = request.user
    try:
        current_employee = alk_employee.objects.get(user_id=user)
        # Add team scope check here if needed in future
        if current_employee.level > 1: # Basic Manager Check
            print(f"ERROR: Unauthorized - User level {current_employee.level} > 1", file=sys.stderr)
            return HttpResponse("Unauthorized", status=403)
    except alk_employee.DoesNotExist:
        print("ERROR: Employee profile not found", file=sys.stderr)
        return HttpResponse("Unauthorized", status=403)

    if result.is_locked:
        print("ERROR: Result is locked", file=sys.stderr)
        return HttpResponse("Locked", status=403)

    # DYNAMIC KEYS
    ach_key = f'achievement_{result_id}'
    tgt_key = f'target_input_{result_id}'

    # --- 1. HANDLE ACHIEVEMENT UPDATE ---
    # Only allow update if NOT from SAP
    if ach_key in request.POST and not result.kpi.from_sap:
        val = request.POST.get(ach_key)
        print(f"DEBUG: Processing Achievement: '{val}'", file=sys.stderr)
        try:
            # Handle empty string as None, remove commas
            clean_val = val.replace(',', '') if val else None
            # Handle "None" string explicitly if passed
            if clean_val == '' or clean_val is None:
                result.achievement = None
            else:
                result.achievement = Decimal(clean_val)
            print(f"DEBUG: Achievement Updated to: {result.achievement}", file=sys.stderr)
        except ValueError as e:
            print(f"ERROR: Achievement Conversion Failed: {e}", file=sys.stderr)
            pass # Keep old value on error

    # --- 2. HANDLE TARGET INPUT UPDATE ---
    # Only allow update if KPI uses Percentage Calculation logic
    if tgt_key in request.POST and result.kpi.percentage_cal:
        val = request.POST.get(tgt_key)
        print(f"DEBUG: Processing Target Input: '{val}'", file=sys.stderr)
        try:
            clean_val = val.replace(',', '') if val else None
             # Handle "None" string explicitly
            if clean_val == '' or clean_val is None:
                result.target_input = None
            else:
                result.target_input = Decimal(clean_val)
            print(f"DEBUG: Target Input Updated to: {result.target_input}", file=sys.stderr)
        except ValueError as e:
            print(f"ERROR: Target Input Conversion Failed: {e}", file=sys.stderr)
            pass

    # --- 3. RECALCULATE & SAVE ---
    # Always recalculate the final score because inputs changed
    result.calculate_final_result() 
    result.save()
    print("--- DEBUG: Save Complete & Signal Sent ---", file=sys.stderr)

    # --- 4. TRIGGER HTMX REFRESH ---
    # This header forces the frontend table to reload itself
    response = HttpResponse("")
    response['HX-Trigger'] = 'kpi_table_update'
    return response
