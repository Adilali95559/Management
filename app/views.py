from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from .models import Employee,Role,Department
# from app.models import Contact
from django.contrib import messages
from . import forms
from .import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.db.models import Q
def index(request):
    return render(request, "base.html")


def quiz(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
         login(request,user)
    # A backend authenticated the credentials
         messages.success(request, 'Your are login !')
         return render(request,"index.html")
        else:
    # No backend authenticated the credentials
         messages.success(request, 'Invalid username or password !')
         return render(request, "quiz.html")
        
    return render(request, "quiz.html")     

def home(request):
    
    return render(request, "base.html")

def register(request):
    form=forms.RegisterUser
    if request.method=='POST':
        form=forms.RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your are register!')

    return render(request, "registert.html",{'form':form})



def logoutUser(request):
    logout(request)
    return redirect('/quiz')

def EmployeeManagement(request):
    emps=Employee.objects.all()
    context={
        'emps': emps
    }
    return render(request,'EmployeeManagement.html',context)

def add_emp(request):
        emps=Employee.objects.all()
        context={
        'emps': emps
    }
        if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            salary=int(request.POST['salary'])
            bonus=int(request.POST['bonus'])
            phone=int(request.POST['phone'])
            role=int(request.POST['role'])
            dept=int(request.POST['dept'])
            

            new_emp=Employee(first_name=first_name,last_name=last_name,salary=salary,bonus=bonus,phone=phone,role_id=role,dept_id=dept,hire_date=datetime.now())
            new_emp.save()
            messages.success(request, 'Employee added Successfully')
            return render(request,'EmployeeManagement.html')
        elif request.method == 'GET':
            return render(request,'EmployeeManagement.html',context)


        else:
         return render(request,'EmployeeManagement.html',context)

def remove_emp(request,emp_id=0):
        emps=Employee.objects.all()
        context={
        'emps': emps
    }
        if emp_id:
            try:
                emp_to_be_remove=Employee.objects.get(id=emp_id)
                emp_to_be_remove.delete()
                messages.success(request, 'Employee Removed Successfully')

                return render(request,'EmployeeManagement.html',context)
            except:
                messages.success(request, "enter a valid id")
                return render(request,'EmployeeManagement.html',context)
        
        return render(request,'EmployeeManagement.html',context)
def filter(request):
    return render(request,'filter_emp.html')

def filter_emp(request):
    if request.method == 'POST':
        name=request.POST['name']
        role=request.POST['role']
        dept=request.POST['dept']
        emps=Employee.objects.all()
        if name:
            emps=emps.filter(Q(first_name__icontains=name) |Q (last_name__icontains= name))
        if role:
            emps=emps.filter(role__name=role)
        if dept:
            emps=emps.filter(dept__name=dept)
        
        context={
        'emps': emps
        }
        return render(request,'EmployeeManagement.html',context)
    elif request.method == 'GET':
        return render(request,'EmployeeManagement.html')
    else:
        messages.success(request, "An Exception Occurred")
        return render(request,'EmployeeManagement.html')





    return render(request,"filter_emp.html")

def LeaveManagement(request):
    return render(request,'LeaveManagement.html')

def AttendanceManagement(request):
    return render(request,'AttendanceManagement.html')

def TeamManagement(request):
    return render(request,'TeamManagement.html')
def ResourceManagement(request):
    return render(request,'ResourceManagement.html')





