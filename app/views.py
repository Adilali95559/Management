from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime, timezone
from .models import Employee, Role, Department, EmpLeaveDetails, EmpAttendanceDetails, TeamMgmt, EmpAssetDetails
# from app.models import Contact
from django.contrib import messages
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.db.models import Q


def index(request):
    return render(request, "base.html")


def createAccount(request):
    form = forms.RegisterUser
    if request.method == 'POST':
        form = forms.RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your are register!')
    return render(request, "createAccount.html", {'form': form})


def quiz(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # A backend authenticated the credentials
            messages.success(request, 'Your are login !')
            return render(request, "index.html")
        else:
            # No backend authenticated the credentials
            messages.success(request, 'Invalid username or password !')
            return render(request, "quiz.html")

    return render(request, "quiz.html")


def home(request):
    return render(request, "base.html")


def register(request):
    form = forms.RegisterUser
    if request.method == 'POST':
        form = forms.RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your are register!')

    return render(request, "registert.html", {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('/quiz')


def EmployeeManagement(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'EmployeeManagement.html', context)


def add_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        role = int(request.POST['role'])
        dept = int(request.POST['dept'])

        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone,
                           role_id=role, dept_id=dept, hire_date=datetime.now())
        new_emp.save()
        messages.success(request, 'Employee added Successfully')
        return render(request, 'EmployeeManagement.html')
    elif request.method == 'GET':
        return render(request, 'EmployeeManagement.html', context)


    else:
        return render(request, 'EmployeeManagement.html', context)


def remove_emp(request, emp_id=0):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    if emp_id:
        try:
            emp_to_be_remove = Employee.objects.get(id=emp_id)
            emp_to_be_remove.delete()
            messages.success(request, 'Employee Removed Successfully')

            return render(request, 'EmployeeManagement.html', context)
        except:
            messages.success(request, "enter a valid id")
            return render(request, 'EmployeeManagement.html', context)

    return render(request, 'EmployeeManagement.html', context)


def filter(request):
    return render(request, 'filter_emp.html')


def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        role = request.POST['role']
        dept = request.POST['dept']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if role:
            emps = emps.filter(role__name=role)
        if dept:
            emps = emps.filter(dept__name=dept)

        context = {
            'emps': emps
        }
        return render(request, 'EmployeeManagement.html', context)
    elif request.method == 'GET':
        return render(request, 'EmployeeManagement.html')
    else:
        messages.success(request, "An Exception Occurred")
        return render(request, 'EmployeeManagement.html')

    return render(request, "filter_emp.html")


def LeaveManagement(request):
    emps_leave = EmpLeaveDetails.objects.all()
    context = {
        'emps_leave': emps_leave
    }
    return render(request, 'LeaveManagement.html', context)


def AttendanceManagement(request):
    emps_attendance = EmpAttendanceDetails.objects.all()
    context = {
        'emps_attendance': emps_attendance
    }
    return render(request, 'AttendanceManagement.html', context)


def TeamManagement(request):
    emps_team = TeamMgmt.objects.all()
    context = {
        'emps_team': emps_team
    }
    return render(request, 'TeamManagement.html', context)


def ResourceManagement(request):
    emps_asset = EmpAssetDetails.objects.all()
    context = {
        'emps_asset': emps_asset
    }
    return render(request, 'ResourceManagement.html', context)


def apply_emp_leave(request):
    emps_leave = EmpLeaveDetails.objects.all()
    context = {
        'emps_leave': emps_leave
    }

    if request.method == 'POST':
        emp_name = request.POST['emp_name']
        leave_type = request.POST['leave_type']
        leave_request_from = request.POST['leave_request_from']
        leave_request_to = request.POST['leave_request_to']
        leave_request_status = request.POST['leave_request_status']
        leave_request_approved_by = request.POST['leave_request_approved_by']

        new_emp = EmpLeaveDetails(emp_name=emp_name, leave_type=leave_type, leave_request_date=datetime.now(),
                                  leave_request_from=datetime.now(), leave_request_to=datetime.now(),
                                  leave_request_status=leave_request_status,
                                  leave_request_approved_by=leave_request_approved_by, )
        new_emp.save()
        messages.success(request, 'Leave applied Successfully')
        return render(request, 'LeaveManagement.html')
    elif request.method == 'GET':
        return render(request, 'LeaveManagement.html', context)


    else:
        return render(request, 'LeaveManagement.html', context)


def add_emp_attendance(request):
    emps_attendance = EmpAttendanceDetails.objects.all()
    context = {
        'emps_attendance': emps_attendance
    }

    if request.method == 'POST':
        emp_name = request.POST['emp_name']
        swipe_in = request.POST['swipe_in']
        swipe_out = request.POST['swipe_out']
        total_hours = 9
        full_or_half_day = 'Full'

        new_emp = EmpAttendanceDetails(emp_name=emp_name, swipe_in=datetime.now(), swipe_out=datetime.now(),
                                       total_hours=total_hours,
                                       full_or_half_day=full_or_half_day,
                                       )
        new_emp.save()
        messages.success(request, 'Attendance logged Successfully')
        return render(request, 'AttendanceManagement.html')
    elif request.method == 'GET':
        return render(request, 'AttendanceManagement.html', context)


    else:
        return render(request, 'AttendanceManagement.html', context)

def add_team(request):
    emps_team = TeamMgmt.objects.all()
    context = {
        'emps_team': emps_team
    }

    if request.method == 'POST':
        emp_name = request.POST['emp_name']
        team_type = request.POST['team_type']
        designation = request.POST['designation']
        experience = request.POST['experience']
        project = request.POST['project']


        new_emp = TeamMgmt(emp_name=emp_name, team_type=team_type, designation=designation,
                                       experience=experience,
                                       project=project,
                                       )
        new_emp.save()
        messages.success(request, 'Team Member Successfully')
        return render(request, 'TeamManagement.html')
    elif request.method == 'GET':
        return render(request, 'TeamManagement.html', context)


    else:
        return render(request, 'TeamManagement.html', context)

def add_asset(request):
    emps_asset = EmpAssetDetails.objects.all()
    context = {
        'emps_asset': emps_asset
    }

    if request.method == 'POST':
        emp_name = request.POST['emp_name']
        asset_type = request.POST['asset_type']
        asset_id = request.POST['asset_id']
        assigned_date = request.POST['assigned_date']
        return_date = request.POST['return_date']

        new_emp = EmpAssetDetails(emp_name=emp_name, asset_type=asset_type, asset_id=asset_id,
                                  assigned_date=datetime.now(), return_date=datetime.now(),

                                  )
        new_emp.save()
        messages.success(request, 'Asset Assigned Successfully')
        return render(request, 'ResourceManagement.html')
    elif request.method == 'GET':
        return render(request, 'ResourceManagement.html', context)


    else:
        return render(request, 'ResourceManagement.html', context)
