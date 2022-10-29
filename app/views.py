from datetime import datetime

# from app.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from . import forms
from .decorators import admin_only
from .models import Employee, Role, Department, EmpLeaveDetails, EmpAttendanceDetails, TeamMgmt, EmpAssetDetails


def index(request):
    return render(request, "base.html")


def createAccount(request):
    form = forms.RegisterUser
    if request.method == 'POST':
        form = forms.RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your are register!')
        else:
            messages.success(request, 'invalid Entry')
    return render(request, "createAccount.html", {'form': form})


def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            context = {
                'user': user
            }
            login(request, user)
            # A backend authenticated the credentials
            messages.success(request, f'Your are login ! {user}')
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
    return redirect('/log_in')


@login_required
@admin_only
def EmployeeManagement(request):
    username = request.user.username
    emp_names = ''
    if username != 'admin':
        emps = Employee.objects.filter(username=username).values()
        emp_id = ''
        for emp in emps:
            emp_id = int(emp['emp_id'])

        emps = Employee.objects.filter(emp_id=emp_id).values()
    else:
        emps = Employee.objects.all()

    userlist = User.objects.all()
    emps_role = Role.objects.all()
    all_department = Department.objects.all()
    context = {
        'emps': emps,
        'userslist': userlist,
        'emps_role': emps_role,
        'all_department': all_department
    }

    return render(request, 'EmployeeManagement.html', context)


@login_required
@admin_only
def add_emp(request):
    username = request.user.username

    if username != 'admin':
        emps = Employee.objects.filter(username=username).values()
        emp_id = ''
        for emp in emps:
            emp_id = int(emp['emp_id'])

        emps = Employee.objects.filter(emp_id=emp_id).values()
    else:
        emps = Employee.objects.all()

    userlist = User.objects.all()
    context = {
        'emps': emps,
        'userslist': userlist
    }
    
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        role = int(request.POST['role'])
        dept = int(request.POST['dept'])

        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone,
                           role_id=role, dept_id=dept, hire_date=datetime.now(), username=username)
        new_emp.save()
        messages.success(request, 'Employee added Successfully')
        return render(request, 'EmployeeManagement.html', context)
    elif request.method == 'GET':
        return render(request, 'EmployeeManagement.html', context)


    else:
        return render(request, 'EmployeeManagement.html', context)


@login_required
@admin_only
def remove_emp(request, emp_id=0):
    username = request.user.username
    if username != 'admin':
        emps = Employee.objects.filter(username=username).values()
        emp_id = ''
        for emp in emps:
            emp_id = int(emp['emp_id'])

        emps = Employee.objects.filter(emp_id=emp_id).values()
    else:
        emps = Employee.objects.all()
    userlist = User.objects.all()
    context = {
        'emps': emps,
        'userslist': userlist
    }
    if emp_id:
        try:
            emp_to_be_remove = Employee.objects.get(emp_id=emp_id)
            emp_to_be_remove.delete()
            messages.success(request, 'Employee Removed Successfully')

            return render(request, 'EmployeeManagement.html', context)
        except:
            messages.success(request, "enter a valid id")
            return render(request, 'EmployeeManagement.html', context)

    return render(request, 'EmployeeManagement.html', context)


@login_required
@admin_only
def filter(request):
    return render(request, 'filter_emp.html')


@login_required
@admin_only
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
        return render(request, 'EmployeeManagement.html', )
    else:
        messages.success(request, "An Exception Occurred")
        return render(request, 'EmployeeManagement.html', )

    return render(request, "filter_emp.html", context)


@login_required
def LeaveManagement(request):
    username = request.user.username
    emp_names = ''
    if username != 'admin':
        emps = Employee.objects.filter(username=username).values()
        if not emps:
            messages.error(request, 'Please on Board this user as employee then use Leave Management Feature.')
            return render(request, 'LeaveManagement.html')
        emp_id = ''
        for emp in emps:
            emp_id = emp['emp_id']
            emp_names = emp['first_name'] + emp['last_name']
            
        emps_leave = EmpLeaveDetails.objects.filter(emp_id=emp_id).values()
    else:
        emps_leave = EmpLeaveDetails.objects.all()
    context = {
        'emps_leave': emps_leave,
        'emp_names': emp_names,
        'username' : username
    }
    return render(request, 'LeaveManagement.html', context)


@login_required
def AttendanceManagement(request):
    username = request.user.username
    emp_names = ''
    if username != 'admin':
        emps = Employee.objects.filter(username=username).values()
        if not emps:
            messages.error(request, 'Please on Board this user as employee then use Attendance Management Feature.')
            return render(request, 'AttendanceManagement.html')
        emp_id = ''
        for emp in emps:
            emp_id = emp['emp_id']
            emp_names = emp['first_name'] + emp['last_name']
        emps_attendance = EmpAttendanceDetails.objects.filter(emp_id=emp_id).values()
    else:
        emps_attendance = EmpAttendanceDetails.objects.all()

    context = {
        'emps_attendance': emps_attendance,
        'emp_names': emp_names,
        'username' : username
    }
    return render(request, 'AttendanceManagement.html', context)


@login_required
@admin_only
def TeamManagement(request):
    username = request.user.username
    emp_names = ''
    if username != 'admin':
        emps = Employee.objects.filter(username=username).values()
        emp_id = ''
        for emp in emps:
            emp_id = int(emp['emp_id'])
            emp_names = emp['last_name'] + ' ' + emp['last_name']
        emps_team = TeamMgmt.objects.filter(emp_id=emp_id).values()
    else:
        emps_team = TeamMgmt.objects.all()
        emps = Employee.objects.all()

    userlist = User.objects.all()
    

    context = {
        'emps_team': emps_team,
        'emp_names': emp_names,
        'userslist': userlist
    }


    return render(request, 'TeamManagement.html', context)


@login_required
@admin_only
def ResourceManagement(request):
    username = request.user.username
    emp_names = ''
    if username != 'admin':
        emps = Employee.objects.filter(username=username).values()
        emp_id = ''
        for emp in emps:
            emp_id = int(emp['emp_id'])
            emp_names = emp['last_name'] + ' ' + emp['last_name']
        emps_asset = EmpAssetDetails.objects.filter(emp_id=emp_id).values()
        emp_instance = Employee.objects.get(emp_id=emp_id)
    else:
        
        emps_asset = EmpAssetDetails.objects.all()
        emps = Employee.objects.all()

    userlist = User.objects.all()
    

    context = {
        'emps_asset': emps_asset,
        'emp_names': emp_names,
        'userslist': userlist
    }
    return render(request, 'ResourceManagement.html', context)


@login_required
def apply_emp_leave(request):
    username = request.user.username
    emp_names = ''
    if username != 'admin':
        emps = Employee.objects.filter(username=username).values()
        if not emps:
            messages.error(request, 'Please on Board this user as employee then use Leave Management Feature.')
            return render(request, 'LeaveManagement.html')
        emp_id = ''
        for emp in emps:
            emp_id = int(emp['emp_id'])
            emp_names = emp['last_name'] + ' ' + emp['last_name']
        emps_leave = EmpLeaveDetails.objects.filter(emp_id=emp_id).values()
        emp_instance = Employee.objects.get(emp_id=emp_id)
    else:
        emps_leave = EmpLeaveDetails.objects.all()

    context = {
        'emps_leave': emps_leave,
        'emp_names': emp_names
    }

    if request.method == 'POST':
        emp_name = request.POST['emp_name']
        leave_type = request.POST['leave_type']
        leave_request_from = request.POST['leave_request_from']
        leave_request_to = request.POST['leave_request_to']
        leave_request_status = 'Waiting For Approval'
        leave_request_approved_by = 'NA'

        new_emp = EmpLeaveDetails(emp_id=emp_instance, emp_name=emp_name, leave_type=leave_type,
                                  leave_request_date=datetime.now(),
                                  leave_request_from=leave_request_from, leave_request_to=leave_request_to,
                                  leave_request_status=leave_request_status,
                                  leave_request_approved_by=leave_request_approved_by, )
        new_emp.save()
        messages.success(request, 'Leave applied Successfully')
        return render(request, 'LeaveManagement.html', context)
    elif request.method == 'GET':
        return render(request, 'LeaveManagement.html', context)


    else:
        return render(request, 'LeaveManagement.html', context)


@login_required
def add_emp_attendance(request):
    username = request.user.username
    emp_names = ''
    if username != 'admin':
        emps = Employee.objects.filter(username=username).values()
        if not emps:
            messages.error(request, 'Please on Board this user as employee then use Attendance Management Feature.')
            return render(request, 'AttendanceManagement.html')
        emp_id = ''
        for emp in emps:
            emp_id = int(emp['emp_id'])
            emp_names = emp['last_name'] + ' ' + emp['last_name']
        emps_attendance = EmpAttendanceDetails.objects.filter(emp_id=emp_id).values()
        emp_instance = Employee.objects.get(emp_id=emp_id)
    else:
        emps_attendance = EmpAttendanceDetails.objects.all()

    context = {
        'emps_attendance': emps_attendance,
        'emp_names': emp_names
    }

    if request.method == 'POST':
        emp_name = request.POST['emp_name']
        swipe_in = request.POST['swipe_in']
        swipe_out = request.POST['swipe_out']
        swipe_in_time = datetime.strptime(swipe_in, '%Y-%m-%dT%H:%M')
        swipe_out_time = datetime.strptime(swipe_out, '%Y-%m-%dT%H:%M')
        target_date = str(swipe_out_time - swipe_in_time)

        if target_date.__contains__('day'):
            total_time = 24
        else:
            total_time = int(target_date.split(':')[0])

        if 9 > total_time > 0:

            total_hours = total_time
            full_or_half_day = 'half'

        elif total_time <= 0:
            total_hours = 0
            full_or_half_day = 'absent'
        else:
            total_hours = total_time
            full_or_half_day = 'Full'

        new_emp = EmpAttendanceDetails(emp_id=emp_instance, emp_name=emp_name, swipe_in=swipe_in, swipe_out=swipe_out,
                                       total_hours=total_hours,
                                       full_or_half_day=full_or_half_day,
                                       )
        new_emp.save()
        messages.success(request, 'Attendance logged Successfully')
        return render(request, 'AttendanceManagement.html', context)
    elif request.method == 'GET':
        return render(request, 'AttendanceManagement.html', context)


    else:
        return render(request, 'AttendanceManagement.html', context)


@login_required
@admin_only
def add_team(request):
    
    if request.method == 'POST':
        
        user_name = request.POST['user_name']
        emps = Employee.objects.filter(username=user_name).values()
        if not emps:
            messages.error(request, 'Please on Board this user as employee then only add as team member')
            return render(request, 'TeamManagement.html')
        emp_id = ''
        
        for emp in emps:
            emp_id = int(emp['emp_id'])
            emp_names = emp['first_name'] + '' +emp['last_name']
        emp_instance = Employee.objects.get(emp_id=emp_id)
        team_type = request.POST['team_type']
        designation = request.POST['designation']
        experience = request.POST['experience']
        project = request.POST['project']

        new_emp = TeamMgmt(emp_id=emp_instance, emp_name=emp_names, team_type=team_type, designation=designation,
                           experience=experience,
                           project=project,
                           )
        new_emp.save()
        emps_asset = TeamMgmt.objects.all()
        context = {
            'emps_asset': emps_asset,
            'emp_names': emp_names
        }
        messages.success(request, 'Team Member Successfully')
        return render(request, 'TeamManagement.html', context)
    elif request.method == 'GET':
        emps_asset = TeamMgmt.objects.all()
        context = {
            'emps_asset': emps_asset,

        }
        return render(request, 'TeamManagement.html', context)


    else:
        emps_asset = TeamMgmt.objects.all()
        context = {
            'emps_asset': emps_asset,

        }
        return render(request, 'TeamManagement.html', context)


@login_required
@admin_only
def add_asset(request):

    if request.method == 'POST':
        user_name = request.POST['user_name']
        emps = Employee.objects.filter(username=user_name).values()
        if not emps:
            messages.error(request, 'Please on Board this user as employee then only assign asset')
            return render(request, 'ResourceManagement.html')

        emp_id = ''
        for emp in emps:
            emp_id = int(emp['emp_id'])
            emp_names = emp['first_name'] + emp['last_name']
        emp_instance = Employee.objects.get(emp_id=emp_id)

        asset_type = request.POST['asset_type']
        asset_id = request.POST['asset_id']
        assigned_date = request.POST[
            'assigned_date']
        return_date = request.POST['return_date']

        new_emp = EmpAssetDetails(emp_id=emp_instance, emp_name=emp_names, asset_type=asset_type, asset_id=asset_id,
                                  assigned_date=datetime.now(), return_date=return_date,

                                  )
        new_emp.save()
        emps_asset = EmpAssetDetails.objects.all()
        context = {
            'emps_asset': emps_asset,
            'emp_names': emp_names
        }
        messages.success(request, 'Asset Assigned Successfully')
        return render(request, 'ResourceManagement.html', context)
    elif request.method == 'GET':
        emps_asset = EmpAssetDetails.objects.all()
        context = {
            'emps_asset': emps_asset,
        }
        return render(request, 'ResourceManagement.html', context)


    else:
        emps_asset = EmpAssetDetails.objects.all()
        context = {
            'emps_asset': emps_asset,
        }

        return render(request, 'ResourceManagement.html', context)
