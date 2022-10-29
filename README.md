## Employee Management Application
  Employee Management System is a distributed application, developed to maintain the details of employees working in any organization. It maintains the information about the personal details of their employees, It guides and manages employees efforts in the right direction. It also securely stores and manages personal and other work-related details for your employees.
## List of Technology and platform used to build this App.

1. Python as Backend language .
2. Django as Web Framework.
3. SQLite as Backend database.
4. GitHub to maintain repository.

## List of Feature supported 
  **As a Admin**
1. **Employee Management** : Admin can use this feature to on board the employee once employee account is created or signup.
2. **Team Management** : Admin can use this feature to build a Team which is already an employee.
3. **Asset/Resource Management** : Admin can use this feature to assign assets to employee for their workstation .
4. **Leave Management** : Admin can use this feature to approve the leave requested by an employee .
5. **Attendance Management** : Admin can use this feature to view the attendance of the employee.

  **As a Employee**

1. **Leave Management** : Employee can use this feature to apply the leave .
2. **Attendance Management** : Employee can use this feature log the attendance .

## How to use Employee Management System App.

1. Install python 3.8 or above
2. Clone the repository https://github.com/Adilali95559/Management.git  
   Get inside the repo directory
3. Create python virtual env  
   **python -m venv ems**
4. Activate virtual environment  
   **.\ems\Scripts\activate**
5. Install Django==4.1.2  
   **pip install Django==4.1.2**
6. Run database migration command .

   **python manage.py makemigrations**

   **python manage.py migrate**

7. Start the server 
   python .\manage.py runserver 8080
8. Creat superuser
   python manage.py createsuperuser
   


## Note : Admin user will be available no need to create again.
