from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index,name='index'),
    path('log_in', views.log_in ,name='log_in'),
    path('home', views.home ,name='home'),
    path('register', views.register ,name='register'),
    path('logout', views.logoutUser ,name='logout'),
    path('EmployeeManagement', views.EmployeeManagement ,name='EmployeeManagement'),
    path('LeaveManagement', views.LeaveManagement ,name='LeaveManagement'),
    path('AttendanceManagement', views.AttendanceManagement ,name='AttendanceManagement'),
    path('TeamManagement', views.TeamManagement ,name='TeamManagement'),
    path('ResourceManagement', views.ResourceManagement ,name='ResourceManagement'),
    path('add_emp', views.add_emp ,name='add_emp'),
    path('remove_emp', views.remove_emp ,name='remove_emp'),
    path('remove_emp/<int:emp_id>', views.remove_emp ,name='remove_emp'),
    path('filter_emp', views.filter_emp ,name='filter_emp'),
    path('filter', views.filter ,name='filter'),
    path('createAccount', views.createAccount ,name='createAccount'),
    path('apply_emp_leave', views.apply_emp_leave ,name='apply_emp_leave'),
    path('add_emp_attendance', views.add_emp_attendance ,name='add_emp_attendance'),
    path('add_team', views.add_team ,name='add_team'),
    path('add_asset', views.add_asset ,name='add_asset'),
    
]
