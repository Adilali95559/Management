from django.contrib import admin
from .models import Employee, Role, Department, EmpLeaveDetails

admin.site.register(Employee)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(EmpLeaveDetails)
