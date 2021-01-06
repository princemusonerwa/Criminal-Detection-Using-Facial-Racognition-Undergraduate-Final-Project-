from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import StudentForm, EmployeeForm, CrimeForm
from .models import Student, Employee, Crime, Department, Faculty, Gallery, Person
from django.contrib import messages
from .detection import train, predictKNN
from django.core.files.storage import FileSystemStorage
import cv2
from .task import detect as notify
from .task import trainData as trainData
from django.contrib.auth.decorators import login_required
from datetime import datetime
import csv
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from io import BytesIO
import xlwt

# Create your views here.

@login_required
def addStudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST , request.FILES)
        files = request.FILES.getlist('images')        
        if form.is_valid():
            form.save()
            for f in files:
                Gallery.objects.create(person=form.instance.person_ptr,photos=f)  

            messages.success(request, 'Student created Successfully.')   
            return redirect('students')
            
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form':form})

def allStudent(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students':students})

@login_required
def train_images(request):
    train()
    messages.success(request, "Image trained successfully.")
    return redirect('detect')

def detect(request):
    return render(request, "detect.html")


def studentDetails(request, id):
    student = get_object_or_404(Student, student_id = id)
    gallery = student.gallery_set.all()
    context = {
        'student' : student,
        'gallery': gallery,
    }
    return render(request, 'students/student_detail.html', context)

def deleteStudent(request, id):
    student = Student.objects.get(student_id = id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted Successfully.')
        return redirect('students')
    return render(request, 'students/student_confirm_delete.html', {'student':student})

def deleteImage(request, id):
    image = Gallery.objects.get(id = id)
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted Successfully.')
        trainData.delay()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def addImage(request, id):
    if request.method == 'POST':
        person = Person.objects.get(id = id)
        files = request.FILES.getlist('images')        
        for f in files:
            Gallery.objects.create(person= person,photos=f) 
        trainData.delay()    
        messages.success(request, 'Image added Successfully.')
        if(hasattr(person,"student")): 
            student_id = person.student.student_id 
            return redirect('student_details',str(student_id))  
        if(hasattr(person,"employee")): 
            staff_id = person.employee.staff_id 
            return redirect('employee_details',str(staff_id))
    else:
        return render(request, 'gallery/image_form.html')

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
        files = request.FILES.getlist('images')
        if form.is_valid():
            form.save()
            for f in files:
                Gallery.objects.create(person=form.instance.person_ptr,photos=f) 
                
            messages.success(request, 'Employee created Successfully.')
            return redirect('employees')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form':form})


def allEmployee(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees':employees})

def employeeDetails(request, id):
    employee = get_object_or_404(Employee, staff_id = id)
    gallery = employee.gallery_set.all()
    context = {
        'employee' : employee,
        'gallery' : gallery,
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


def detect_criminal(request):
    if  request.method == 'POST':
        cap = cv2.VideoCapture(0)
        while(True): 
            # Capture frame-by-frame
            ret, image = cap.read()
            # to speed up the process, we will resize the image captured 
            image_small = cv2.resize(image, (0,0), None, 0.25, 0.25)
            # convert the frame image to RGB
           
            # create uncodings for our faces in the image 
            predictions=predictKNN(image_small)
           
            for name,loc in predictions:
                if name != "unknown":
                    notify.delay(name,"gishushu")

                y1,x2,y2,x1 = loc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(image, (x1,y1), (x2,y2), (255,0,0), 2)
                cv2.rectangle(image, (x1,y2-20), (x2,y2), (255,0,0), cv2.FILLED)
                cv2.putText(image, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255,0), 2)

            # Display the resulting frame
            cv2.imshow('frame',image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

def detect_image(request):
    # This is an example of running face recognition on a single image
    # and drawing a box around each person that was identified.

    # Load a sample picture and learn how to recognize it.

    #upload image
    name = ""
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        image = cv2.imread(uploaded_file_url[1:])
        print(uploaded_file_url[1:])
        predictions=predictKNN(image) 

        for pred_name,loc in predictions:
            name = pred_name
    return render(request, 'detect.html', {'name':name})

def exportStudentListCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']= 'attachement; filename=StudentList'+ str(datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['student_id', 'names', 'Dob', 'status'])
    students = Student.objects.all()
    for student in students:
        writer.writerow([student.student_id, student.names, student.dob,student.status])
    
    return response

def exportStudentListPdf(request):
    path = "students/pdf_page.html"
    students = Student.objects.all()
    context = {"students" : students}

    html = render_to_string('students/pdf_page.html',context)
    io_bytes = BytesIO()
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
    if not pdf.err:
        # we can just return the HttpResponse
        response = HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
        response['Content-Disposition']= 'inline; filename=StudentList'+ str(datetime.now())+'.pdf'
        return response
    else:
        return HttpResponse("Error while rendering PDF", status=400)

def exportStudentListexcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']= 'attachement; filename=StudentList'+ str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['student_id', 'names', 'Dob', 'status']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Student.objects.all().values_list('student_id', 'names', 'dob', 'status')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
        
    wb.save(response)

    return response

def exportEmployeeListCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']= 'attachement; filename=TeacherList'+ str(datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['staff_id', 'names', 'Dob', 'status', 'Address', 'Phone'])
    employees = Employee.objects.all()
    for employee in employees:
        writer.writerow([employee.staff_id, employee.names, employee.dob, employee.status, employee.address, employee.phone])
    
    return response

def exportEmployeeListPdf(request):
    path = "employees/pdf_page.html"
    employees = Employee.objects.all()
    context = {"employees" : employees}

    html = render_to_string('employees/pdf_page.html',context)
    io_bytes = BytesIO()
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
    if not pdf.err:
        # we can just return the HttpResponse
        response = HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
        response['Content-Disposition']= 'inline; filename=EmployeeList'+ str(datetime.now())+'.pdf'
        return response
    else:
        return HttpResponse("Error while rendering PDF", status=400)

def exportEmployeeListExcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']= 'attachement; filename=EmployeeList'+ str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Teachers')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['staff_id', 'names', 'Dob', 'status']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Employee.objects.all().values_list('staff_id', 'names', 'dob', 'status')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
        
    wb.save(response)

    return response