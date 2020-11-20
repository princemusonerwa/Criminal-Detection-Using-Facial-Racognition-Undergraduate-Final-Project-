from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import StudentForm, EmployeeForm, CrimeForm
from .models import Student, Employee, Crime, Department, Faculty
from django.contrib import messages

# Create your views here.

def addStudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students')
            messages.success(request, 'Student created Successfully.')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form':form})

def allStudent(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students':students})

def studentDetails(request, id):
    student = get_object_or_404(Student, student_id = id)
    context = {
        'student' : student
    }
    return render(request, 'students/student_detail.html', context)

def deleteStudent(request, id):
    student = Student.objects.get(student_id = id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted Successfully.')
        return redirect('students')
    return render(request, 'students/student_confirm_delete.html', {'student':student})

def updateStudent(request, id):
    obj = get_object_or_404(Student, student_id = id) 
    # pass the object as instance in form 
    form = StudentForm(request.POST or None, instance = obj) 
    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated Successfully.')
        return redirect('/student/'+str(id))
    return render(request, 'students/student_form.html', {'form':form})

def addEmployee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')
            messages.success(request, 'Employee created Successfully.')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form':form})


def allEmployee(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees':employees})

def employeeDetails(request, id):
    employee = get_object_or_404(Employee, staff_id = id)
    context = {
        'employee' : employee
    }
    return render(request, 'employees/employee_detail.html', context)

def deleteEmployee(request, id):
    employee = Employee.objects.get(staff_id = id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted Successfully.')
        return redirect('employees')
    return render(request, 'employees/employee_confirm_delete.html', {'employee':employee})

def updateEmployee(request, id):
    obj = get_object_or_404(Employee, staff_id = id) 
    # pass the object as instance in form 
    form = EmployeeForm(request.POST or None, instance = obj) 
    if form.is_valid():
        form.save()
        messages.success(request, 'Employee updated Successfully.')
        return redirect('/employee/'+str(id))
    return render(request, 'employees/employee_form.html', {'form':form})

def addCrime(request):
    if request.method == 'POST':
        form = CrimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crimes')
            messages.success(request, 'Crime created Successfully.')
    else:
        form = CrimeForm()
    return render(request, 'crimes/crime_form.html', {'form':form})

def allCrime(request):
    crimes = Crime.objects.all()
    return render(request, 'crimes/crime_list.html', {'crimes':crimes})

def crimeDetails(request, id):
    crime = get_object_or_404(Crime, id = id)
    context = {
        'crime' : crime
    }
    return render(request, 'crimes/crime_detail.html', context)

def deleteCrime(request, id):
    crime = Crime.objects.get(id = id)
    if request.method == 'POST':
        crime.delete()
        messages.success(request, 'Crime deleted Successfully.')
        return redirect('crimes')
    return render(request, 'crimes/crime_confirm_delete.html', {'crime':crime})

def updateCrime(request, id):
    obj = get_object_or_404(Crime, id = id) 
    # pass the object as instance in form 
    form = CrimeForm(request.POST or None, instance = obj) 
    if form.is_valid():
        form.save()
        messages.success(request, 'Crime updated Successfully.')
        return redirect('/crime/'+str(id))
    return render(request, 'crimes/crime_form.html', {'form':form})

def loadDepartments(request):
    faculty_id = request.GET.get('faculty')
    departments = Department.objects.filter(faculty_id=faculty_id).order_by('name')
    return render(request, 'students/department_dropdown_list_options.html', {'departments': departments})