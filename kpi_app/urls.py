from django.contrib import admin
from django.urls import path, include
from . import views
from .views import portal_views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('accounts/logout/', views.user_logout, name='accounts_logout'),
    path('export-alk-kpi-result/', views.export_alk_kpi_result, name='export_alk_kpi_result'),  # Thêm url xuất báo cáo
    path('manage/', views.manage_kpi_result, name='manage_kpi_result'),

    # PORTAL URLS
    path('portal/', portal_views.dashboard, name='portal_dashboard'),
    path('portal/manager/', portal_views.manager_dashboard, name='manager_dashboard'),
    path('portal/manager/review/<int:emp_id>/', portal_views.manager_review_employee, name='manager_review_employee'),
    path('portal/manager/toggle-approval/<int:emp_id>/', portal_views.manager_toggle_approval, name='manager_toggle_approval'),
    path('portal/input/', portal_views.input_form, name='portal_input'),
    path('portal/input/<int:year>/<str:semester>/<str:month>/', portal_views.input_form, name='portal_input_params'),
    path('portal/save-kpi/<int:result_id>/', portal_views.save_kpi_result, name='portal_save_kpi'),
    path('portal/manager/save/<int:result_id>/', portal_views.manager_save_kpi, name='manager_save_kpi'),
]
