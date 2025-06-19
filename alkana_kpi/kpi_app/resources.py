from import_export import resources, fields
from import_export.widgets import BooleanWidget, ForeignKeyWidget, Widget

from .models import alk_dept, alk_job_title, alk_kpi, alk_perspective, alk_dept_objective, alk_dept_group, alk_employee, alk_kpi_result
from django.contrib.auth.models import User

# Lớp tài nguyên cho model alk_dept, dùng để import/export dữ liệu phòng ban.
class alk_deptResource(resources.ModelResource):
    # Định nghĩa trường dept_name và active để ánh xạ với cột tương ứng trong file import/export.
    dept_name = fields.Field(attribute='dept_name', column_name='dept_name')
    active = fields.Field(attribute='active', column_name='active', widget=BooleanWidget())
    class Meta:
        model = alk_dept
        import_id_fields = ('dept_name',)  # Sử dụng dept_name làm khóa định danh khi import.
        fields = ('dept_name', 'active')   # Chỉ import/export hai trường này.

# Lớp tài nguyên cho model alk_job_title, dùng để import/export dữ liệu chức danh công việc.
class alk_job_titleResource(resources.ModelResource):
    # Định nghĩa trường job_title và active.
    job_title = fields.Field(attribute='job_title', column_name='job_title')
    active = fields.Field(attribute='active', column_name='active', widget=BooleanWidget())
    class Meta:
        model = alk_job_title
        import_id_fields = ('job_title',)  # Sử dụng job_title làm khóa định danh khi import.
        fields = ('job_title', 'active')

# Lớp tài nguyên cho model alk_perspective, dùng để import/export dữ liệu góc nhìn KPI.
class alk_perspectiveResource(resources.ModelResource):
    # Định nghĩa trường perspective_name và active.
    perspective_name = fields.Field(attribute='perspective_name', column_name='perspective_name')
    active = fields.Field(attribute='active', column_name='active', widget=BooleanWidget())
    class Meta:
        model = alk_perspective
        import_id_fields = ('perspective_name',)  # Sử dụng perspective_name làm khóa định danh khi import.
        fields = ('perspective_name', 'active')

# Lớp tài nguyên cho model alk_dept_objective, dùng để import/export dữ liệu mục tiêu phòng ban.
class alk_dept_objectiveResource(resources.ModelResource):
    # Định nghĩa trường objective_name và active.
    objective_name = fields.Field(attribute='objective_name', column_name='objective_name')
    active = fields.Field(attribute='active', column_name='active', widget=BooleanWidget())
    class Meta:
        model = alk_dept_objective
        import_id_fields = ('objective_name',)  # Sử dụng objective_name làm khóa định danh khi import.
        fields = ('objective_name', 'active')

# Lớp tài nguyên cho model alk_dept_group, dùng để import/export dữ liệu nhóm phòng ban.
class alk_dept_groupResource(resources.ModelResource):
    # Định nghĩa trường group_name và active.
    group_name = fields.Field(attribute='group_name', column_name='group_name')
    active = fields.Field(attribute='active', column_name='active', widget=BooleanWidget())
    class Meta:
        model = alk_dept_group
        import_id_fields = ('group_name',)  # Sử dụng group_name làm khóa định danh khi import.
        fields = ('group_name', 'active')
class alk_employeeResource(resources.ModelResource):
    # Định nghĩa các trường cần thiết cho nhân viên.
    user_id = fields.Field(
        attribute='user_id',  # đúng tên trường ForeignKey trong model
        column_name='user_id',  # đúng header file Excel
        widget=ForeignKeyWidget(User, 'username')  # ánh xạ username, không phải id
    )
    name = fields.Field(attribute='name', column_name='name', default='')
    job_title = fields.Field(
        column_name='job_title',
        attribute='job_title',
        widget=ForeignKeyWidget(alk_job_title, 'job_title')
    )
    dept = fields.Field(
        column_name='dept',
        attribute='dept',
        widget=ForeignKeyWidget(alk_dept, 'dept_name')
    )
    dept_gr = fields.Field(
        column_name='dept_gr',
        attribute='dept_gr',
        widget=ForeignKeyWidget(alk_dept_group, 'group_name')
    )
    level = fields.Field(attribute='level', column_name='level')
    active = fields.Field(attribute='active', column_name='active', widget=BooleanWidget())
    class Meta:
        model = alk_employee
        import_id_fields = ('user_id',)  # Sử dụng user_id làm khóa định danh khi import.
        fields = ('user_id','name', 'dept','dept_gr', 'job_title', 'level', 'active')  # Chỉ import/export các trường này.

# Lớp tài nguyên cho model alk_kpi, dùng để import/export dữ liệu KPI.
class alk_kpiResource(resources.ModelResource):
    kpi_name = fields.Field(attribute='kpi_name', column_name='kpi_name')
    kpi_type = fields.Field(attribute='kpi_type', column_name='kpi_type')
    perspective = fields.Field(
        column_name='perspective',
        attribute='perspective',
        widget=ForeignKeyWidget(alk_perspective, 'perspective_name')
    )
    dept_obj = fields.Field(
        column_name='dept_obj',
        attribute='dept_obj',
        widget=ForeignKeyWidget(alk_dept_objective, 'objective_name')
    )
    from_sap = fields.Field(attribute='from_sap', column_name='from_sap', widget=BooleanWidget())
    active = fields.Field(attribute='active', column_name='active', widget=BooleanWidget())
    is_percentage = fields.Field(attribute='percentage_cal', column_name='percentage_cal', widget=BooleanWidget())
    get_1_zero= fields.Field(attribute='get_1_is_zero', column_name='get_1_is_zero', widget=BooleanWidget())

    class Meta:
        model = alk_kpi
        import_id_fields = ('kpi_name',)
        fields = ('kpi_name', 'perspective','dept_obj',  'kpi_type', 'percentage_cal', 'get_1_is_zero','from_sap', 'active')
    # Chỉ import/export các trường này.

class EmployeeUsernameWidget(Widget):
    def clean(self, value, row=None, *args, **kwargs):
        from .models import alk_employee
        try:
            return alk_employee.objects.get(user_id__username=value)
        except alk_employee.DoesNotExist:
            raise Exception(f"Không tìm thấy nhân viên với username: {value}")
    def render(self, value, obj=None):
        return value.user_id.username if value and value.user_id else ''

class AlkKpiResultImportResource(resources.ModelResource):
    year = fields.Field(attribute='year', column_name='year')
    semester = fields.Field(attribute='semester', column_name='semester')
    employee = fields.Field(
        attribute='employee',
        column_name='employee',
        widget=EmployeeUsernameWidget()
    )
    kpi = fields.Field(
        attribute='kpi',
        column_name='kpi',
        widget=ForeignKeyWidget(alk_kpi, 'kpi_name')
    )
    weigth = fields.Field(attribute='weigth', column_name='weigth')
    target_set = fields.Field(attribute='target_set', column_name='target_set')
    achivement = fields.Field(attribute='achivement', column_name='achivement')
    month = fields.Field(attribute='month', column_name='month')

    class Meta:
        model = alk_kpi_result
        import_id_fields = ('year', 'semester', 'employee', 'kpi', 'month')
        fields = (
            'year', 'semester', 'employee', 'kpi', 'weigth', 'target_set','achivement', 'month'
        )
        export_order = fields
class AlkKpiResultExportResource(resources.ModelResource):
    get_dept = fields.Field(column_name='get_dept')
    get_employee_userid = fields.Field(column_name='get_employee_userid')
    get_employee_name = fields.Field(column_name='get_employee_name')
    get_level = fields.Field(column_name='get_level')
    get_job_title = fields.Field(column_name='get_job_title')
    get_perspective = fields.Field(column_name='get_perspective')
    get_dept_obj = fields.Field(column_name='get_dept_obj')
    get_kpi_name = fields.Field(column_name='get_kpi_name')
    weigth_percent_1f = fields.Field(column_name='weigth_percent_1f')
    min_1f = fields.Field(column_name='min_1f')
    target_set_1f = fields.Field(column_name='target_set_1f')
    max_1f = fields.Field(column_name='max_1f')
    target_input_1f = fields.Field(column_name='target_input_1f')
    achivement_1f = fields.Field(column_name='achivement_1f')
    final_result_percent_1f = fields.Field(column_name='final_result_percent_1f')
    get_kpi_type = fields.Field(column_name='get_kpi_type')
    get_percentage_cal = fields.Field(column_name='get_percentage_cal')
    get_get_1_is_zero = fields.Field(column_name='get_get_1_is_zero')
    get_kpi_from_sap = fields.Field(column_name='get_kpi_from_sap')
    def dehydrate_get_dept(self, obj):
        return obj.employee.dept.dept_name if obj.employee and obj.employee.dept else ''
    def dehydrate_get_employee_userid(self, obj):
        return obj.employee.user_id.username if obj.employee and obj.employee.user_id else ''
    def dehydrate_get_employee_name(self, obj):
        return obj.employee.name if obj.employee else ''
    def dehydrate_get_level(self, obj):
        return obj.employee.level if obj.employee else ''
    def dehydrate_get_job_title(self, obj):
        return obj.employee.job_title.job_title if obj.employee and obj.employee.job_title else ''
    def dehydrate_get_perspective(self, obj):
        return obj.kpi.perspective.perspective_name if obj.kpi and obj.kpi.perspective else ''
    def dehydrate_get_dept_obj(self, obj):
        return obj.kpi.dept_obj.objective_name if obj.kpi and obj.kpi.dept_obj else ''
    def dehydrate_get_kpi_name(self, obj):
        return obj.kpi.kpi_name if obj.kpi else ''
    def dehydrate_weigth_percent_1f(self, obj):
        return f"{round(obj.weigth * 100, 1)}%" if obj.weigth is not None else ''
    def dehydrate_min_1f(self, obj):
        return f"{round(obj.min, 1)}" if obj.min is not None else ''
    def dehydrate_target_set_1f(self, obj):
        return f"{round(obj.target_set, 1)}" if obj.target_set is not None else ''
    def dehydrate_max_1f(self, obj):
        return f"{round(obj.max, 1)}" if obj.max is not None else ''
    def dehydrate_target_input_1f(self, obj):
        return f"{round(obj.target_input, 1)}" if obj.target_input is not None else ''
    def dehydrate_achivement_1f(self, obj):
        return f"{round(obj.achivement, 1)}" if obj.achivement is not None else ''
    def dehydrate_final_result_percent_1f(self, obj):
        return f"{round(obj.final_result * 100, 1)}%" if obj.final_result is not None else ''
    def dehydrate_get_kpi_type(self, obj):
        kpi_type_map = {
            1: "1 - Bigger better result = achieve/target",
            2: "2 - Smaller better result = target/achieve",
            3: "3 - Mistake"
        }
        return kpi_type_map.get(obj.kpi.kpi_type, obj.kpi.kpi_type) if obj.kpi else ''
    def dehydrate_get_percentage_cal(self, obj):
        return obj.kpi.percentage_cal if obj.kpi else ''
    def dehydrate_get_get_1_is_zero(self, obj):
        return obj.kpi.get_1_is_zero if obj.kpi else ''
    def dehydrate_get_kpi_from_sap(self, obj):
        return obj.kpi.from_sap if obj.kpi else ''

    class Meta:
        model = alk_kpi_result
        export_order = (
            'year',
            'semester',
            'get_dept',
            'get_employee_userid',
            'get_employee_name',
            'get_level',
            'get_job_title',
            'get_perspective',
            'get_dept_obj',
            'get_kpi_name',
            'weigth_percent_1f',
            'min_1f',
            'target_set_1f',
            'max_1f',
            'target_input_1f',
            'achivement_1f',
            'final_result_percent_1f',
            'month',
            'get_kpi_type',
            'get_percentage_cal',
            'get_get_1_is_zero',
            'get_kpi_from_sap',
        )