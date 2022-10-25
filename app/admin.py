from django.contrib import admin
from .models import Employee, Role, Department, EmpLeaveDetails, EmpAttendanceDetails, TeamMgmt, EmpAssetDetails

admin.site.register(Employee)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(EmpLeaveDetails)
admin.site.register(EmpAttendanceDetails)
admin.site.register(TeamMgmt)
admin.site.register(EmpAssetDetails)