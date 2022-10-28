from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.IntegerField(default=0)
    hire_date = models.DateField()
    username = models.CharField(max_length=50, unique=True,default='NA')

    def __str__(self):
        return "%s %s %s" % (self.first_name, self.last_name, self.phone)


class EmpLeaveDetails(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    emp_name = models.CharField(max_length=30)
    leave_type = models.CharField(max_length=30)
    leave_request_date = models.DateField()
    leave_request_from = models.DateField()
    leave_request_to = models.DateField()
    leave_request_status = models.CharField(max_length=30)
    leave_request_approved_by = models.CharField(max_length=30)


class EmpAttendanceDetails(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    emp_name = models.CharField(max_length=30)
    swipe_in = models.DateTimeField()
    swipe_out = models.DateTimeField()
    total_hours = models.IntegerField()
    full_or_half_day = models.CharField(max_length=30)


class TeamMgmt(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    emp_name = models.CharField(max_length=30)
    team_type = models.CharField(max_length=30)
    designation = models.CharField(max_length=30)
    experience = models.CharField(max_length=30)
    project = models.CharField(max_length=30)


class EmpAssetDetails(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    emp_name = models.CharField(max_length=30)
    asset_type = models.CharField(max_length=30)
    asset_id = models.CharField(max_length=30)
    assigned_date = models.DateTimeField()
    return_date = models.DateTimeField()
