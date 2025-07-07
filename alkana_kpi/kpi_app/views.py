from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import alk_employee, alk_job_title, alk_dept, alk_dept_group, alk_kpi_result
from django.contrib.auth import update_session_auth_hash
import csv
import pandas as pd
from django.core.paginator import Paginator
git add kpi_app/templates/kpi_app/home.html

@login_required
def home(request):
    user = request.user
    try:
        employee = alk_employee.objects.get(user_id=user)
        user_dept = alk_dept.objects.filter(alk_employee__user_id=user).distinct()
    except alk_employee.DoesNotExist:
        user_dept = alk_dept.objects.none()

    # Lấy các tham số lọc từ request
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    month = request.GET.get('month')
    user_id = request.GET.get('user_id')
    name = request.GET.get('name')

    report_data = None
    page_obj = None
    if any([year, semester, month, user_id, name]) or user.is_superuser:
        results = alk_kpi_result.objects.all()
        if not user.is_superuser:
            # Lọc theo bộ phận của employee có user_id là username của user đang đăng nhập
            try:
                employee = alk_employee.objects.get(user_id=user)
                results = results.filter(employee__dept=employee.dept)
            except alk_employee.DoesNotExist:
                results = results.none()
        if year:
            results = results.filter(year=year)
        if semester:
            results = results.filter(semester=semester)
        if month:
            results = results.filter(month=month)
        if user_id:
            results = results.filter(employee__user_id__username__icontains=user_id)
        if name:
            results = results.filter(employee__name__icontains=name)
        from django.db.models import Sum
        report_data = results.values(
            'year', 'semester', 'month',
            'employee__user_id__username', 'employee__name', 'employee__dept__dept_name'
        ).annotate(subtotal=Sum('final_result'))
        paginator = Paginator(report_data, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, 'kpi_app/home.html', {
        'user_dept': user_dept,
        'report_data': page_obj if page_obj else report_data,
        'filters': {
            'year': year or '',
            'semester': semester or '',
            'month': month or '',
            'user_id': user_id or '',
            'name': name or '',
        }
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            from django.contrib.auth.forms import AuthenticationForm
            form = AuthenticationForm(request, data=request.POST)
            return render(request, 'registration/login.html', {'form': form})
    else:
        from django.contrib.auth.forms import AuthenticationForm
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    try:
        employee = alk_employee.objects.get(user_id=user)
    except alk_employee.DoesNotExist:
        employee = None
    if request.method == 'POST':
        # Đổi mật khẩu nếu có dữ liệu
        if request.POST.get('old_password') and request.POST.get('new_password1') and request.POST.get('new_password2'):
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if not user.check_password(old_password):
                messages.error(request, 'Mật khẩu cũ không đúng.')
            elif new_password1 != new_password2:
                messages.error(request, 'Mật khẩu mới không khớp.')
            elif len(new_password1) < 6:
                messages.error(request, 'Mật khẩu mới phải có ít nhất 6 ký tự.')
            else:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Đổi mật khẩu thành công!')
        else:
            # Cập nhật thông tin nhân viên
            if employee:
                emp_name = request.POST.get('emp_name', '').strip()
                if not emp_name:
                    messages.error(request, 'Tên nhân viên không được để trống.')
                else:
                    employee.name = emp_name
                    job_title_id = request.POST.get('job_title')
                    dept_id = request.POST.get('dept')
                    dept_gr_id = request.POST.get('dept_gr')
                    level = request.POST.get('level')
                    if job_title_id:
                        employee.job_title_id = int(job_title_id)
                    if dept_id:
                        employee.dept_id = int(dept_id)
                    if dept_gr_id:
                        employee.dept_gr_id = int(dept_gr_id)
                    if level:
                        employee.level = int(level)
                    employee.save()
                    messages.success(request, 'Cập nhật thông tin thành công!')
    # Lấy danh sách cho dropdown
    job_titles = alk_job_title.objects.all()
    depts = alk_dept.objects.all()
    dept_grs = alk_dept_group.objects.all()
    level_choices = alk_employee.LEVEL_CHOICES
    return render(request, 'kpi_app/profile.html', {
        'employee': employee,
        'job_titles': job_titles,
        'depts': depts,
        'dept_grs': dept_grs,
        'level_choices': level_choices,
    })

def export_alk_kpi_result(request):
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    month = request.GET.get('month')
    user_id = request.GET.get('user_id')
    name = request.GET.get('name')

    results = alk_kpi_result.objects.all()
    if year:
        results = results.filter(year=year)
    if semester:
        results = results.filter(semester=semester)
    if month:
        results = results.filter(month=month)
    if user_id:
        results = results.filter(employee__user_id__username__icontains=user_id)
    if name:
        results = results.filter(employee__name__icontains=name)

    from django.db.models import Sum
    grouped = results.values(
        'year', 'semester', 'month',
        'employee__user_id__username', 'employee__name', 'employee__dept__dept_name'
    ).annotate(subtotal=Sum('final_result'))

    # Xuất ra Excel
    df = pd.DataFrame(list(grouped))
    df.rename(columns={
        'year': 'Year',
        'semester': 'Semester',
        'month': 'Month',
        'employee__user_id__username': 'Employee User ID',
        'employee__name': 'Employee Name',
        'employee__dept__dept_name': 'Department',
        'subtotal': 'Subtotal (Final Result)'
    }, inplace=True)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="alk_kpi_result_report.xlsx"'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='KPI Report')
    return response





