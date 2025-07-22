from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class alk_dept(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['dept_name']
        verbose_name_plural = "Department"  # Optional: Custom plural name for the model
    def __str__(self):
        return self.dept_name
    
class alk_job_title(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['job_title']
        verbose_name_plural = "Job Title"
    def __str__(self):
        return self.job_title
class alk_perspective(models.Model):
    perspective_id = models.AutoField(primary_key=True)
    perspective_name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['perspective_name']
        verbose_name_plural = "Perspective"  # Optional: Custom plural name for the model
    def __str__(self):
        return self.perspective_name
class alk_dept_objective(models.Model):
    objective_id = models.AutoField(primary_key=True)
    objective_name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['objective_name']
        verbose_name_plural = "Department Objective"  # Optional: Custom plural name for the model
    def __str__(self):
        return self.objective_name
class alk_dept_group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['group_name']  
        verbose_name_plural = "Department Group"   
    def __str__(self):
        return self.group_name
class alk_employee(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='')
    job_title = models.ForeignKey('alk_job_title', on_delete=models.CASCADE)
    dept = models.ForeignKey('alk_dept', on_delete=models.CASCADE)
    dept_gr = models.ForeignKey('alk_dept_group', on_delete=models.CASCADE)
    LEVEL_CHOICES = [
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Level 4'),
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['dept','name', 'job_title']
        verbose_name_plural = "Employee"

    def __str__(self):
        return f"{self.user_id.username} - {self.job_title.job_title}"
class alk_kpi(models.Model):
    KPI_TYPE_CHOICES = [
        (1, "1 - Bigger better result = achieve/target"),
        (2, "2 - Smaller better result = target/achieve"),
        (3, "3 - Mistake"),
    ]
    kpi_name = models.CharField(max_length=200)
    dept_obj = models.ForeignKey('alk_dept_objective', on_delete=models.CASCADE)
    perspective = models.ForeignKey('alk_perspective', on_delete=models.CASCADE)
    #kpi_type = models.IntegerField(choices=KPI_TYPE_CHOICES)
    kpi_type = models.IntegerField(choices=KPI_TYPE_CHOICES, default=1)  # Default to "1 - Bigger better result"
    from_sap = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    percentage_cal= models.BooleanField(default=False)
    get_1_is_zero= models.BooleanField(default=False)
    percent_display = models.BooleanField(default=False,null=True, blank=True)


    class Meta:
        ordering = ['kpi_name']
        verbose_name_plural = "KPI"

    def __str__(self):
        return self.kpi_name
class alk_kpi_result(models.Model):
    SEMESTER_CHOICES = [
        ('1st SEM', '1st SEM'),
        ('2nd SEM', '2nd SEM'),
    ]
    MONTH_CHOICES = [
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('4th', '4th'),
        ('5th', '5th'),
        ('final', 'Final'),
    ]

    year = models.IntegerField()
    semester = models.CharField(max_length=7, choices=SEMESTER_CHOICES)
    employee = models.ForeignKey('alk_employee', on_delete=models.CASCADE)
    kpi = models.ForeignKey('alk_kpi', on_delete=models.CASCADE)
    weigth = models.DecimalField(max_digits=20, decimal_places=3,null=True)
    min = models.DecimalField(max_digits=20, decimal_places=3, default=0.4)
    target_set = models.DecimalField(max_digits=20, decimal_places=4,null=True)
    max = models.DecimalField(max_digits=20, decimal_places=3, default=1.4)
    target_input = models.DecimalField(max_digits=20, decimal_places=4,null=True, blank=True)
    achivement = models.DecimalField(max_digits=20, decimal_places=4,null=True, blank=True)
    month = models.CharField(max_length=6, choices=MONTH_CHOICES)
    final_result = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True,editable=False)
    active = models.BooleanField(default=True)

    def calculate_final_result(self):
        # Nếu target_input hoặc achivement là None thì final_result = 0
        if self.target_input is None or self.achivement is None:
            return 0
        temp_result = 0
        temp_achive = 0
        # Lấy các biến cần thiết
        achivement = self.achivement or 0
        target_set = self.target_set or 0
        target_input = self.target_input or 0
        weigth = self.weigth or 0
        min_val = self.min or 0
        max_val = self.max or 0
        kpi_type = self.kpi.kpi_type if self.kpi else None
        percentage_cal = self.kpi.percentage_cal if self.kpi else False
        get_1_is_zero = self.kpi.get_1_is_zero if self.kpi else False

        if get_1_is_zero:
            if achivement > 0:
                return 0
            else:
                return weigth * max_val
        else:
            if kpi_type == 3:
                if achivement == 0:
                    temp_result = max_val
                else:
                    temp_result = target_set / achivement if achivement else 0
            else:
                if percentage_cal:
                    temp_achive = achivement / target_input if target_input else 0
                    if kpi_type == 1:
                        temp_result = temp_achive / target_set if target_set else 0
                    elif kpi_type == 2:
                        temp_result = target_set / temp_achive if temp_achive else 0
                else:
                    if kpi_type == 1:
                        temp_result = achivement / target_input if target_input else 0
                    elif kpi_type == 2:
                        temp_result = target_input / achivement if achivement else 0
        # Xử lý theo min/max
        if temp_result < min_val:
            return 0
        if temp_result > max_val:
            return max_val * weigth
        return temp_result * weigth
    
        
    def save(self, *args, **kwargs):
        # Nếu kpi.percentage_cal = False thì target_input = target_set
        if self.kpi and hasattr(self.kpi, 'percentage_cal') and self.kpi.percentage_cal is False:
            self.target_input = self.target_set
        self.final_result = self.calculate_final_result()
        super().save(*args, **kwargs)
    class Meta:
        ordering = ['year', 'semester', 'employee', 'kpi','month',]
        verbose_name_plural = "KPI Result"
    def __str__(self):
        return f"{self.employee} - {self.kpi} ({self.year} {self.semester})"