from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import alk_dept, alk_job_title, alk_kpi, alk_perspective, alk_dept_objective, alk_dept_group, alk_employee, alk_kpi_result
from .resources import AlkKpiResultImportResource, AlkKpiResultExportResource
from .resources import alk_deptResource, alk_job_titleResource, alk_perspectiveResource, alk_dept_objectiveResource, alk_dept_groupResource, alk_employeeResource, alk_kpiResource
from django.contrib.admin import SimpleListFilter
from django.db import models
from django.utils.safestring import mark_safe
#test

# Đăng ký model alk_dept với giao diện admin, hỗ trợ import/export và các tuỳ chỉnh hiển thị.
class alk_deptAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Quản trị phòng ban (alk_dept) trong admin:
    - Hỗ trợ import/export dữ liệu phòng ban.
    - Hiển thị, tìm kiếm, lọc và phân trang danh sách phòng ban.
    """
    resource_class = alk_deptResource  # Sử dụng resource để import/export.
    list_display = ('dept_id', 'dept_name', 'group', 'active')  # Hiển thị các trường này trong danh sách.
    search_fields = ('dept_name', 'group')  # Cho phép tìm kiếm theo tên phòng ban và nhóm.
    list_filter = ( 'group', 'active',)  # Lọc theo trạng thái hoạt động.
    # list_editable = ('dept_name', 'active')  # Cho phép chỉnh sửa trực tiếp các trường này.
    list_per_page = 15  # Phân trang, mỗi trang 15 dòng

# Đăng ký model alk_job_title với giao diện admin, hỗ trợ import/export và các tuỳ chỉnh hiển thị.
class alk_job_titleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Quản trị chức danh công việc (alk_job_title) trong admin.
    """
    resource_class = alk_job_titleResource
    list_display = ('job_id', 'job_title', 'active')
    search_fields = ('job_title',)
    list_filter = ('active',)
    list_per_page = 15

# Đăng ký model alk_perspective với giao diện admin, hỗ trợ import/export và các tuỳ chỉnh hiển thị.
class alk_perspectiveAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Quản trị góc nhìn (alk_perspective) trong admin.
    """
    resource_class = alk_perspectiveResource
    list_display = ('perspective_id', 'perspective_name', 'active')
    search_fields = ('perspective_name',)
    list_filter = ('active',)
    list_per_page = 15

# Đăng ký model alk_dept_objective với giao diện admin, hỗ trợ import/export và các tuỳ chỉnh hiển thị.
class alk_dept_objectiveAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Quản trị mục tiêu phòng ban (alk_dept_objective) trong admin.
    """
    resource_class = alk_dept_objectiveResource
    list_display = ('objective_id', 'objective_name', 'active')
    search_fields = ('objective_name',)
    list_filter = ('active',)
    list_per_page = 15

# Đăng ký model alk_dept_group với giao diện admin, hỗ trợ import/export và các tuỳ chỉnh hiển thị.
class alk_dept_groupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Quản trị nhóm phòng ban (alk_dept_group) trong admin.
    """
    resource_class = alk_dept_groupResource
    list_display = ('group_id', 'group_name', 'active')
    search_fields = ('group_name',)
    list_filter = ('active',)  
    list_per_page = 15

class alk_employeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Quản trị nhân viên (alk_employee) trong admin.
    - Hiển thị thông tin nhân viên, phòng ban, nhóm, chức danh, cấp bậc, trạng thái.
    - Hỗ trợ tìm kiếm, lọc và phân trang.
    """
    resource_class = alk_employeeResource
    list_display = ('user_id','name', 'dept','dept_gr', 'job_title',   'level', 'active')
    search_fields = ('user_id__username','name' ,'job_title__job_title', 'dept__dept_name', 'dept_gr__group_name')
    list_filter = ('active','dept', 'dept_gr', 'job_title',   'level')
    list_per_page = 20

# Đăng ký model alk_kpi với giao diện admin, hỗ trợ import/export và các tuỳ chỉnh hiển thị.
class alk_kpiAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Quản trị KPI (alk_kpi) trong admin.
    - Hiển thị các trường liên quan đến KPI.
    - Hỗ trợ tìm kiếm, lọc và phân trang.
    """
    resource_class = alk_kpiResource
    list_display = ('kpi_name', 'perspective', 'dept_obj', 'kpi_type', 'percentage_cal', 'get_1_is_zero','from_sap','percent_display' ,'active')
    search_fields = ('kpi_name',)
    list_filter = ('active',)
    list_per_page = 15
    # list_editable = ('dept_obj', 'perspective', 'kpi_type', 'from_sap', 'active')
    # list_display_links = None

class AlkKpiResultAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        # Superuser được edit tất cả
        if request.user.is_superuser:
            return super().has_change_permission(request, obj)
        # Các user khác chỉ edit khi active=True
        if obj is not None and hasattr(obj, 'active') and not obj.active:
            return False
        return super().has_change_permission(request, obj)
    """
    Quản trị kết quả KPI (alk_kpi_result) trong admin.
    - Hỗ trợ import/export với resource riêng.
    - Hiển thị chi tiết các trường liên quan đến kết quả KPI.
    - Phân quyền xem/sửa theo user, employee level, trạng thái KPI.
    - Tùy chỉnh readonly cho các trường dựa trên logic nghiệp vụ.
    """
    def get_import_resource_class(self):
        # Resource dùng cho import dữ liệu
        return AlkKpiResultImportResource

    def get_export_resource_class(self):
        # Resource dùng cho export dữ liệu
        return AlkKpiResultExportResource

    list_display = (
        'year',
        'semester',
        'get_dept',
        # 'get_employee_userid',
        'get_employee_name',
        # 'get_level',
        'get_job_title',
        # 'get_perspective',
        # 'get_dept_obj',
        'get_kpi_name',
        'weigth_percent_1f',
        'min_1f',
        'target_set_1f',
        # 'target_set',
        'max_1f',
        'target_input_1f',
        'achivement_1f',
        'factor_percent_1f',  # Thêm cột Factor ở đây
        'final_result_percent_1f',
        'month',
        'get_kpi_type',
        'get_percentage_cal',
        'get_get_1_is_zero',
        'get_kpi_from_sap',
    )
    fields = [
        'year', 'semester', 'employee', 'kpi', 'weigth', 'min', 'target_set', 'max',
        'target_input', 'achivement', 'month'
    ]
    list_per_page = 15
    list_display_links = ('get_kpi_name',)  # Cho phép nhấp vào tên KPI để xem chi tiết
    # list_editable = ('target_input', 'achivement','month')
    readonly_fields = ('year', 'semester', 'weigth', 'target_set', 'month', 'min', 'final_result')

    search_fields = ('year', 'semester', 'employee__name', 'employee__user_id__username', 'kpi__kpi_name')
    list_filter = (
        'year', 'semester', 'month',
        'kpi__kpi_type',
        'kpi__percentage_cal',
        'kpi__get_1_is_zero',
        'kpi__from_sap',
    )

    class Media:
        # Thêm CSS cho giao diện admin (cuộn ngang)
        css = {
            'all': ('kpi_app/css/admin_horizontal_scroll.css',)
        }

    # Các hàm get_* dùng để hiển thị thông tin liên kết từ các model liên quan
    def get_employee_name(self, obj):
        """Lấy tên nhân viên từ đối tượng alk_employee."""
        return obj.employee.name
    get_employee_name.short_description = 'Employee Name'

    def get_dept(self, obj):
        """Lấy tên phòng ban của nhân viên."""
        return obj.employee.dept.dept_name
    get_dept.short_description = 'Dept'

    def get_level(self, obj):
        """Lấy cấp bậc của nhân viên."""
        return obj.employee.level
    get_level.short_description = 'Level'

    def get_job_title(self, obj):
        """Lấy chức danh công việc của nhân viên."""
        return obj.employee.job_title.job_title
    get_job_title.short_description = 'Job Title'

    def get_perspective(self, obj):
        """Lấy tên góc nhìn của KPI."""
        return obj.kpi.perspective.perspective_name
    get_perspective.short_description = 'Perspective'

    def get_dept_obj(self, obj):
        """Lấy tên mục tiêu phòng ban của KPI."""
        return obj.kpi.dept_obj.objective_name
    get_dept_obj.short_description = 'Dept Obj'

    def get_kpi_name(self, obj):
        """Lấy tên KPI."""
        return obj.kpi.kpi_name
    get_kpi_name.short_description = 'KPI Name'

    def get_kpi_type(self, obj):
        """
        Hiển thị mô tả loại KPI thay vì số.
        1: Lớn hơn tốt hơn, 2: Nhỏ hơn tốt hơn, 3: Lỗi.
        """
        kpi_type_map = {
            1: "1 - Bigger better result = achieve/target",
            2: "2 - Smaller better result = target/achieve",
            3: "3 - Mistake"
        }
        return kpi_type_map.get(obj.kpi.kpi_type, obj.kpi.kpi_type)
    get_kpi_type.short_description = 'KPI Type'

    def get_percentage_cal(self, obj):
        """Lấy trạng thái tính phần trăm của KPI."""
        return obj.kpi.percentage_cal
    get_percentage_cal.short_description = 'Percentage Cal'

    def get_get_1_is_zero(self, obj):
        """Lấy trạng thái get_1_is_zero của KPI."""
        return obj.kpi.get_1_is_zero
    get_get_1_is_zero.short_description = 'Get 1 Is Zero'

    def get_employee_userid(self, obj):
        """Lấy username của nhân viên."""
        return obj.employee.user_id.username if obj.employee and obj.employee.user_id else ''
    get_employee_userid.short_description = 'Employee User ID'

    def get_queryset(self, request):
        """
        Phân quyền xem dữ liệu KPI:
        - Superuser: xem tất cả.
        - Employee level 1: xem KPI của toàn bộ phòng ban.
        - Employee level 0: xem KPI của tất cả employee có cùng alk_dept.group với mình.
        - Khác: chỉ xem KPI của chính mình.
        """
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return qs
        try:
            employee = alk_employee.objects.get(user_id=user)
        except alk_employee.DoesNotExist:
            return qs.none()
        if employee.level == 1:
            # Xem được KPI của toàn bộ phòng ban của employee đó
            return qs.filter(employee__dept=employee.dept)
        elif employee.level == 0:
            # Xem được KPI của tất cả employee có cùng alk_dept.group với mình
            dept_group = employee.dept.group if employee.dept and hasattr(employee.dept, 'group') else None
            if dept_group:
                depts_in_group = alk_dept.objects.filter(group=dept_group)
                return qs.filter(employee__dept__in=depts_in_group)
            else:
                return qs.none()
        else:
            # Chỉ xem KPI của chính mình
            return qs.filter(employee__user_id=user)

    def has_import_permission(self, request):
        """
        Chỉ cho phép superuser sử dụng chức năng import.
        """
        return request.user.is_superuser

    def get_readonly_fields(self, request, obj=None):
        """
        Xác định các trường readonly dựa trên quyền user, trạng thái KPI, logic nghiệp vụ:
        - Superuser: có thể sửa nhiều trường hơn.
        - Employee level 1: có thể sửa kpi, max.
        - Nếu KPI from_sap: trường achivement readonly.
        - Nếu percentage_cal=False: trường target_input readonly.
        """
        ro = list(self.readonly_fields)
        # Đảm bảo 'employee' luôn readonly
        if 'employee' not in ro:
            ro.append('employee')
        user = request.user
        # Kiểm tra nếu user là superuser thì luôn cho sửa kpi và target_set
        if user.is_superuser:
            if 'kpi' in ro:
                ro.remove('kpi')
            if 'target_set' in ro:
                ro.remove('target_set')
            # from_sap: nếu kpi.from_sap True thì achivement readonly
            if obj and obj.kpi and hasattr(obj.kpi, 'from_sap') and obj.kpi.from_sap:
                if 'achivement' not in ro:
                    ro.append('achivement')
            elif 'achivement' in ro:
                ro.remove('achivement')
            return ro
        # Kiểm tra nếu user có employee level 1
        try:
            employee = alk_employee.objects.get(user_id=user)
            if employee.level == 1:
                if 'kpi' in ro:
                    ro.remove('kpi')
                    ro.remove('max')
            else:
                if 'kpi' not in ro:
                    ro.append('kpi')
                    ro.append('max')
        except alk_employee.DoesNotExist:
            if 'kpi' not in ro:
                ro.append('kpi')
        # from_sap: nếu kpi.from_sap True thì achivement readonly
        if obj and obj.kpi and hasattr(obj.kpi, 'from_sap') and obj.kpi.from_sap:
            if 'achivement' not in ro:
                ro.append('achivement')
        elif 'achivement' in ro:
            ro.remove('achivement')
        # Logic target_input readonly giữ nguyên
        if obj and obj.kpi and hasattr(obj.kpi, 'percentage_cal'):
            if obj.kpi.percentage_cal is False:
                if 'target_input' not in ro:
                    ro.append('target_input')
            else:
                if 'target_input' in ro:
                    ro.remove('target_input')
        return ro

    def final_result_percent(self, obj):
        """Hiển thị kết quả cuối cùng dạng phần trăm."""
        if obj.final_result is not None:
            return f"{round(obj.final_result * 100, 1)}%"
        return ''
    final_result_percent.short_description = 'Final Result (%)'

    def target_set_percent(self, obj):
        """
        Hiển thị target_set dạng phần trăm nếu KPI có percentage_cal,
        ngược lại hiển thị giá trị gốc.
        """
        if obj.kpi and hasattr(obj.kpi, 'percentage_cal') and obj.kpi.percentage_cal and obj.target_set is not None:
            return f"{round(obj.target_set * 100, 3)}%"
        return obj.target_set

    def weigth_percent(self, obj):
        """Hiển thị trọng số dạng phần trăm."""
        if obj.weigth is not None:
            return f"{round(obj.weigth * 100, 1)}%"
        return ''
    weigth_percent.short_description = 'Weigth (%)'

    def weigth_percent_1f(self, obj):
        """Hiển thị trọng số dạng phần trăm (1 chữ số thập phân)."""
        if obj.weigth is not None:
            return f"{round(obj.weigth * 100, 1)}%"
        return ''
    weigth_percent_1f.short_description = 'Weigth (%)'

    def min_1f(self, obj):
        """Hiển thị giá trị min với 1 chữ số thập phân."""
        if obj.min is not None:
            return f"{round(obj.min, 1)}"
        return ''
    min_1f.short_description = 'Min'

    def target_set_1f(self, obj):
        """
        Hiển thị target_set với định dạng phần trăm nếu có percentage_cal,
        hoặc nếu percentage_cal=False và target_set<1 thì cũng hiển thị phần trăm,
        hoặc nếu percent_display=True thì luôn hiển thị phần trăm,
        ngược lại hiển thị 4 chữ số thập phân.
        Nếu target_set == 0 thì không hiển thị phần trăm.
        """
        if obj.target_set is not None:
            if obj.target_set == 0:
                return f"{obj.target_set:,.4f}"
            if obj.kpi and hasattr(obj.kpi, 'percent_display') and obj.kpi.percent_display:
                return f"{round(obj.target_set * 100, 3):,.3f}%"
            if obj.kpi and hasattr(obj.kpi, 'percentage_cal'):
                if obj.kpi.percentage_cal:
                    return f"{round(obj.target_set * 100, 3):,.3f}%"
                elif obj.target_set < 1:
                    return f"{round(obj.target_set * 100, 3):,.3f}%"
            return f"{obj.target_set:,.4f}"
        return ''
    target_set_1f.short_description = 'Target Set'

    def max_1f(self, obj):
        """Hiển thị giá trị max với 1 chữ số thập phân."""
        if obj.max is not None:
            return f"{round(obj.max, 1)}"
        return ''
    max_1f.short_description = 'Max'

    def target_input_1f(self, obj):
        """
        Hiển thị target_input với 4 chữ số thập phân,
        hoặc nếu percentage_cal=False và target_set<1 thì hiển thị phần trăm,
        hoặc nếu percent_display=True thì luôn hiển thị phần trăm.
        Nếu target_set == 0 thì không hiển thị phần trăm.
        """
        if obj.target_input is not None:
            if obj.target_set == 0:
                return f"{obj.target_input:,.4f}"
            if obj.kpi and hasattr(obj.kpi, 'percent_display') and obj.kpi.percent_display:
                return f"{round(obj.target_input * 100, 3):,.3f}%"
            if obj.kpi and hasattr(obj.kpi, 'percentage_cal') and obj.kpi.percentage_cal is False and obj.target_set is not None and obj.target_set < 1:
                return f"{round(obj.target_input * 100, 3):,.3f}%"
            return f"{obj.target_input:,.4f}"
        return ''
    target_input_1f.short_description = 'Target Input'

    def achivement_1f(self, obj):
        """
        Hiển thị achivement với 4 chữ số thập phân,
        hoặc nếu percentage_cal=False và target_set<1 thì hiển thị phần trăm,
        hoặc nếu percent_display=True thì luôn hiển thị phần trăm.
        Nếu target_set == 0 thì không hiển thị phần trăm.
        """
        if obj.achivement is not None:
            if obj.target_set == 0:
                return f"{obj.achivement:,.4f}"
            if obj.kpi and hasattr(obj.kpi, 'percent_display') and obj.kpi.percent_display:
                return f"{round(obj.achivement * 100, 3):,.3f}%"
            if obj.kpi and hasattr(obj.kpi, 'percentage_cal') and obj.kpi.percentage_cal is False and obj.target_set is not None and obj.target_set < 1:
                return f"{round(obj.achivement * 100, 3):,.3f}%"
            return f"{obj.achivement:,.4f}"
        return ''
    achivement_1f.short_description = 'Achivement'

    def final_result_percent_1f(self, obj):
        """Hiển thị kết quả cuối cùng dạng phần trăm (1 chữ số thập phân)."""
        if obj.final_result is not None:
            return f"{round(obj.final_result * 100, 1)}%"
        return ''
    final_result_percent_1f.short_description = 'Final Result (%)'

    def get_kpi_from_sap(self, obj):
        """Hiển thị trạng thái KPI lấy từ SAP."""
        return obj.kpi.from_sap if obj.kpi else ''
    get_kpi_from_sap.short_description = 'Is From SAP'

    def factor_percent_1f(self, obj):
        """
        Hiển thị hệ số (factor) dạng phần trăm, tính bằng final_result / weigth.
        """
        if obj.final_result is not None and obj.weigth:
            try:
                value = obj.final_result / obj.weigth
                return f"{round(value * 100, 1)}%"
            except Exception:
                return ''
        return ''
    factor_percent_1f.short_description = 'Factor (%)'

class KpiUserFilter(SimpleListFilter):
    """
    Bộ lọc KPI theo user:
    - Superuser: xem tất cả KPI.
    - Employee level 0: xem KPI của tất cả employee có cùng alk_dept.group với mình.
    - Employee level 1: xem KPI của phòng ban.
    - Khác: chỉ xem KPI đã có bản ghi alk_kpi_result cho employee đó.
    """
    title = 'kpi'
    parameter_name = 'kpi'

    def lookups(self, request, model_admin):
        user = request.user
        if user.is_superuser:
            kpis = alk_kpi.objects.all()
        else:
            try:
                employee = alk_employee.objects.get(user_id__username=user.username)
            except alk_employee.DoesNotExist:
                return []
            if employee.level == 1:
                # KPI của toàn bộ phòng ban
                kpis = alk_kpi.objects.filter(dept_obj__alk_dept__alk_employee__dept=employee.dept).distinct()
            elif employee.level == 0:
                # KPI của employee có cùng alk_dept.group với alk_dept.group của employee đó
                dept_group = employee.dept.group if employee.dept and hasattr(employee.dept, 'group') else None
                if dept_group:
                    # Lấy tất cả employee thuộc các phòng ban cùng group
                    depts_in_group = alk_dept.objects.filter(group=dept_group)
                    employees_in_group = alk_employee.objects.filter(dept__in=depts_in_group)
                    emp_kpis = alk_kpi_result.objects.filter(employee__in=employees_in_group).values_list('kpi', flat=True)
                    kpis = alk_kpi.objects.filter(id__in=emp_kpis).distinct()
                else:
                    kpis = alk_kpi.objects.none()
            else:
                # KPI chỉ của employee đó (chỉ những KPI đã có bản ghi alk_kpi_result cho employee này)
                emp_kpis = alk_kpi_result.objects.filter(employee=employee).values_list('kpi', flat=True)
                kpis = alk_kpi.objects.filter(id__in=emp_kpis).distinct()
        return [(k.id, k.kpi_name) for k in kpis]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(kpi__id=self.value())
        return queryset

# Đăng ký các model với admin site
admin.site.register(alk_dept, alk_deptAdmin)
admin.site.register(alk_job_title, alk_job_titleAdmin)
admin.site.register(alk_perspective, alk_perspectiveAdmin)
admin.site.register(alk_dept_objective, alk_dept_objectiveAdmin)
admin.site.register(alk_dept_group, alk_dept_groupAdmin)
admin.site.register(alk_employee, alk_employeeAdmin)
admin.site.register(alk_kpi, alk_kpiAdmin)
admin.site.register(alk_kpi_result, AlkKpiResultAdmin)

# Tuỳ chỉnh tiêu đề trang admin
admin.site.site_header = "Alkana KPI App"
admin.site.site_title = "Alkana KPI App"
admin.site.index_title = mark_safe('Welcome to Alkana KPI App | <a href="/home/">Report</a>')


