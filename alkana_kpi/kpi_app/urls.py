from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('accounts/logout/', views.user_logout, name='accounts_logout'),
    path('export-alk-kpi-result/', views.export_alk_kpi_result, name='export_alk_kpi_result'),  # Thêm url xuất báo cáo
]
