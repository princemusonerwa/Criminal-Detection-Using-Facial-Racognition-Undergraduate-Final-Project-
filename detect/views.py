from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import StudentForm, EmployeeForm, CrimeForm, DepartmentForm, FacultyForm, DownloadForm
from .models import Student, Employee, Crime, Department, Faculty, Gallery, Person, Faculty, Department, DetectedCriminal
from django.contrib import messages
from .detection import train, predictKNN
from django.core.files.storage import FileSystemStorage
import cv2
from .task import detect as notify, trainData
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
import csv
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from io import BytesIO
import xlwt
import threading
from datetime import datetime
from weasyprint import HTML
import tempfile

# Create your views here.


@login_required
@user_passes_test(lambda u: u.is_admin)
def addStudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')
        if form.is_valid():
            form.save()
            for f in files:
                Gallery.objects.create(
                    person=form.instance.person_ptr, photos=f)
            trainData.delay()
            messages.success(request, 'Student created Successfully.')
            return redirect('students')
        else:
            print(form.errors)
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})


@login_required
def allStudent(request):
    students = Student.objects.all().order_by('student_id')
    return render(request, 'students/student_list.html', {'students': students})


@login_required
def train_images(request):
    train()
    messages.success(request, "Image trained successfully.")
    return redirect('detect')


def detect(request):
    return render(request, "detect.html")


@login_required
def studentDetails(request, id):
    student = get_object_or_404(Student, student_id=id)
    gallery = student.gallery_set.all()
    profile_image = student.gallery_set.first

    context = {
        'student': student,
        'gallery': gallery,
        'profile_image': profile_image
    }
    return render(request, 'students/student_detail.html', context)


@login_required
def deleteStudent(request, id):
    student = Student.objects.get(student_id=id)
    student.delete()
    messages.success(request, 'Student deleted Successfully.')
    return redirect('students')


def updateStudent(request, id):
    obj = get_object_or_404(Student, student_id=id)
    # pass the object as instance in form
    form = StudentForm(request.POST or request.FILES or None, instance=obj)
    files = request.FILES.getlist('images')
    if form.is_valid():
        form.save()
        for f in files:
            Gallery.objects.create(person=obj, photos=f)
        messages.success(request, 'Student updated Successfully.')
        return redirect('students')
    return render(request, 'students/student_form.html', {'form': form})


@login_required
def updateEmployee(request, id):
    obj = get_object_or_404(Employee, student_id=id)
    # pass the object as instance in form
    form = EmployeeForm(request.POST or request.FILES or None, instance=obj)
    files = request.FILES.getlist('images')
    if form.is_valid():
        form.save()
        for f in files:
            Gallery.objects.create(person=obj, photos=f)
        messages.success(request, 'Employee updated Successfully.')
        return redirect('employees')
    return render(request, 'employees/employee_form.html', {'form': form})


@login_required
def addEmployee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            form.save()
            for f in files:
                Gallery.objects.create(
                    person=form.instance.person_ptr, photos=f)

            messages.success(request, 'Employee created Successfully.')
            return redirect('employees')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})


@login_required
def allEmployee(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})


@login_required
def employeeDetails(request, id):
    employee = get_object_or_404(Employee, staff_id=id)
    gallery = employee.gallery_set.all()
    profile_image = employee.gallery_set.first
    context = {
        'employee': employee,
        'gallery': gallery,
        'profile_image': profile_image
    }
    return render(request, 'employees/employee_detail.html', context)


@login_required
def deleteEmployee(request, id):
    employee = Employee.objects.get(staff_id=id)
    employee.delete()
    messages.success(request, 'Employee deleted Successfully.')
    return redirect('employees')


@login_required
def updateEmployee(request, id):
    obj = get_object_or_404(Employee, staff_id=id)
    # pass the object as instance in form
    form = EmployeeForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Employee updated Successfully.')
        return redirect('employees')
    return render(request, 'employees/employee_form.html', {'form': form})


@login_required
def deleteImage(request, id):
    image = Gallery.objects.get(id=id)
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted Successfully.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def addImage(request, id):
    if request.method == 'POST':
        person = Person.objects.get(id=id)
        files = request.FILES.getlist('images')
        for f in files:
            Gallery.objects.create(person=person, photos=f)
        messages.success(request, 'Image added Successfully.')
        if(hasattr(person, "student")):
            student_id = person.student.student_id
            return redirect('student_details', str(student_id))
        if(hasattr(person, "employee")):
            staff_id = person.employee.staff_id
            return redirect('employee_details', str(staff_id))
    else:
        return render(request, 'gallery/image_form.html')


@login_required
def addCrime(request):
    if request.method == 'POST':
        form = CrimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crimes')
            messages.success(request, 'Crime created Successfully.')
        else:
            print(form.errors)
    else:
        form = CrimeForm()
    return render(request, 'crimes/crime_form.html', {'form': form})


@login_required
def allCrime(request):
    crimes = Crime.objects.all()
    return render(request, 'crimes/crime_list.html', {'crimes': crimes})


@login_required
def crimeDetails(request, id):
    crime = get_object_or_404(Crime, id=id)
    context = {
        'crime': crime
    }
    return render(request, 'crimes/crime_detail.html', context)


@login_required
def deleteCrime(request, id):
    crime = Crime.objects.get(id=id)
    if request.method == 'POST':
        crime.delete()
        messages.success(request, 'Crime deleted Successfully.')
        return redirect('crimes')
    return render(request, 'crimes/crime_confirm_delete.html', {'crime': crime})


@login_required
def updateCrime(request, id):
    obj = get_object_or_404(Crime, id=id)
    # pass the object as instance in form
    form = CrimeForm(request.POST or None, instance=obj)
    if form.is_valid():
        name = form.cleaned_data.get("suspect")
        status = form.cleaned_data.get("status")
        if status == "Under Investigation":
            Person.objects.filter(names=name).update(status='WANTED')
        elif status == "Solved":
            Person.objects.filter(names=name).update(status='NOT WANTED')
        form.save()
        messages.success(request, 'Crime updated Successfully.')
        return redirect('crimes')
    return render(request, 'crimes/crime_form.html', {'form': form})


@login_required
def addFaculty(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculties')
            messages.success(request, 'Faculty created Successfully.')
    else:
        form = FacultyForm()
    return render(request, 'faculties/faculty_form.html', {'form': form})


@login_required
def allFaculty(request):
    faculties = Faculty.objects.all()
    return render(request, 'faculties/faculty_list.html', {'faculties': faculties})


@login_required
def facultyDetails(request, id):
    faculty = get_object_or_404(Faculty, id=id)
    context = {
        'faculty': faculty
    }
    return render(request, 'faculties/faculty_detail.html', context)


@login_required
def deleteFaculty(request, id):
    faculty = Faculty.objects.get(id=id)
    if request.method == 'POST':
        faculty.delete()
        messages.success(request, 'Faculty deleted Successfully.')
        return redirect('faculties')
    return render(request, 'faculties/faculty_confirm_delete.html', {'faculty': faculty})


@login_required
def updateFaculty(request, id):
    obj = get_object_or_404(Faculty, id=id)
    # pass the object as instance in form
    form = FacultyForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Faculty updated Successfully.')
        return redirect('/faculty/'+str(id))
    return render(request, 'faculties/faculty_form.html', {'form': form})


@login_required
def addDepartment(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departments')
            messages.success(request, 'Department created Successfully.')
    else:
        form = DepartmentForm()
    return render(request, 'departements/department_form.html', {'form': form})


@login_required
def allDepartment(request):
    departments = Department.objects.all()
    return render(request, 'departements/department_list.html', {'departments': departments})


@login_required
def departmentDetails(request, id):
    department = get_object_or_404(Department, id=id)
    context = {
        'department': department
    }
    return render(request, 'departements/department_detail.html', context)


@login_required
def deleteDepartment(request, id):
    department = Department.objects.get(id=id)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted Successfully.')
        return redirect('departments')
    return render(request, 'departements/department_confirm_delete.html', {'department': department})


@login_required
def updateDepartment(request, id):
    obj = get_object_or_404(Department, id=id)
    # pass the object as instance in form
    form = DepartmentForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Department updated Successfully.')
        return redirect("departments")
    return render(request, 'departements/department_form.html', {'form': form})


def loadDepartments(request):
    faculty_id = request.GET.get('faculty')
    departments = Department.objects.filter(
        faculty_id=faculty_id).order_by('name')
    return render(request, 'students/department_dropdown_list_options.html', {'departments': departments})


class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID

    def run(self):
        date = datetime.now()
        print(date)
        print(f'Starting at {self.previewName}')
        camPreview(self.previewName, self.camID)


def camPreview(previewName, camID):
    start_time = datetime.now()
    start_time = f'{start_time.year}-{start_time.month}-{start_time.day}-{start_time.hour}-{start_time.minute}-{start_time.second}'
    end_time = None
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    save_path = f'/media/{start_time}__{end_time}.avi'

    out = cv2.VideoWriter(save_path, fourcc, 20.0, (640, 480))
    if cam.isOpened():
        print(f'The time the camera went on is {start_time}')
        ret, frame = cam.read()
    else:
        ret = False

    while ret:
        ret, frame = cam.read()
        # to speed up the process, we will resize the image captured
        image_small = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        # convert the frame image to RGB

        # create uncodings for our faces in the image
        predictions = predictKNN(image_small)

        for name, loc in predictions:
            if name != "unknown":
                if camID == 0:
                    notify.delay(name, "1st Flow")

            y1, x2, y2, x1 = loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.rectangle(frame, (x1, y2-20), (x2, y2),
                          (255, 0, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1+6, y2-6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
        cv2.imshow(previewName, frame)
        # Converts to HSV color space, OCV reads colors as BGR
        # frame is converted to hsv

        out.write(frame)

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    end_time = datetime.now()
    end_time = f'{end_time.year}-{end_time.month}-{end_time.day}-{end_time.hour}-{end_time.minute}-{end_time.second}'
    print(f'The time the camera went off is {end_time}')
    cv2.destroyWindow(previewName)


def detect_criminal(request):
    if request.method == 'POST':
        thread1 = camThread("Camera 1", 0)
        thread1.start()
        return redirect("/detect")


def detect_image(request):
    # This is an example of running face recognition on a single image
    # and drawing a box around each person that was identified.

    # Load a sample picture and learn how to recognize it.

    # upload image
    img_format = {'png', 'jpg', 'bmp', 'jpeg'}
    name = ""
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if uploaded_file_url[1:].split(".")[-1] in img_format:
            image = cv2.imread(uploaded_file_url[1:])
            predictions = predictKNN(image)
            for pred_name, loc in predictions:
                name = pred_name
            name = name.split("_", 1)[1]
        else:
            messages.error(request, f"The file provided is not an image file.")

    return render(request, 'detect.html', {'name': name})


def exportStudentListCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename=StudentList' + \
        str(datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['student_id', 'names', 'Dob', 'status'])
    students = Student.objects.all()
    for student in students:
        writer.writerow([student.student_id, student.names,
                        student.dob, student.status])

    return response


# def exportStudentListPdf(request):
#     path = "students/pdf_page.html"
#     students = Student.objects.all()
#     context = {"students": students}

#     html = render_to_string('students/pdf_page.html', context)
#     io_bytes = BytesIO()

#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)

#     if not pdf.err:
#         # we can just return the HttpResponse
#         response = HttpResponse(io_bytes.getvalue(),
#                                 content_type='application/pdf')
#         response['Content-Disposition'] = 'inline; filename=StudentList' + \
#             str(datetime.now())+'.pdf'
#         return response
#     else:
#         return HttpResponse("Error while rendering PDF", status=400)

def exportStudentListPdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachement; filename=StudentList' + \
        str(datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    students = Student.objects.all().order_by('student_id')
    # render the html page
    html_string = render_to_string(
        'students/pdf_page.html', {'students': students})

    # transfort to html content
    html = HTML(string=html_string)
    result = html.write_pdf()

    # preview the content in the memory
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        # open the pdf and read it for reading
        output.seek(0)
        response.write(output.read())

    return response


def exportStudentListexcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachement; filename=StudentList' + \
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['student_id', 'names', 'email', 'phone', 'gender',
               'dob', 'address', 'status', 'faculty', 'department']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Student.objects.all().values_list('student_id', 'names', 'email', 'phone',
                                             'gender', 'dob', 'address', 'status', 'faculty', 'department')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return redirect("/index")


def exportCrimeListPdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachement; filename=CrimeList' + \
        str(datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    crimes = Crime.objects.all().order_by('updated_at')
    # render the html page
    html_string = render_to_string(
        'crimes/pdf_page.html', {'crimes': crimes})

    # transfort to html content
    html = HTML(string=html_string)
    result = html.write_pdf()

    # preview the content in the memory
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        # open the pdf and read it for reading
        output.seek(0)
        response.write(output.read())

    return response


def exportEmployeeListCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename=TeacherList' + \
        str(datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['staff_id', 'names', 'Dob', 'status', 'Address', 'Phone'])
    employees = Employee.objects.all()
    for employee in employees:
        writer.writerow([employee.staff_id, employee.names, employee.dob,
                        employee.status, employee.address, employee.phone])

    return response


def exportEmployeeListPdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachement; filename=EmployeeList' + \
        str(datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    employees = Employee.objects.all().order_by('staff_id')
    # render the html page
    html_string = render_to_string(
        'employees/pdf_page.html', {'employees': employees})

    # transfort to html content
    html = HTML(string=html_string)
    result = html.write_pdf()

    # preview the content in the memory
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        # open the pdf and read it for reading
        output.seek(0)
        response.write(output.read())

    return response


# def exportEmployeeListPdf(request):
#     path = "employees/pdf_page.html"
#     employees = Employee.objects.all()
#     context = {"employees": employees}

#     html = render_to_string('employees/pdf_page.html', context)
#     io_bytes = BytesIO()

#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)

#     if not pdf.err:
#         # we can just return the HttpResponse
#         response = HttpResponse(io_bytes.getvalue(),
#                                 content_type='application/pdf')
#         response['Content-Disposition'] = 'inline; filename=EmployeeList' + \
#             str(datetime.now())+'.pdf'
#         return response
#     else:
#         return HttpResponse("Error while rendering PDF", status=400)


def exportEmployeeListExcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachement; filename=EmployeeList' + \
        str(datetime.now())+'.xls'
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


def pendingCrimesReport(request):
    if request.POST:
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        searchResult = Crime.objects.filter(
            status="Pending", updated_at__gte=from_date, updated_at__lte=to_date)
        download_form = DownloadForm(initial={
            'from_date': from_date,
            'to_date': to_date
        })
        return render(request, "reports/pending_crimes.html", {'pending_crimes': searchResult, 'download_form': download_form})
    else:
        pending_crimes = Crime.objects.filter(status="Pending")
        return render(request, "reports/pending_crimes.html", {'pending_crimes': pending_crimes})


def solvedCrimesReport(request):
    if request.POST:
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        searchResult = Crime.objects.filter(
            status="Solved", updated_at__gte=from_date, updated_at__lte=to_date)
        download_form = DownloadForm(initial={
            'from_date': from_date,
            'to_date': to_date
        })
        return render(request, "reports/solved_crimes.html", {'solved_crimes': searchResult, 'download_form': download_form})
    else:
        solved_crimes = Crime.objects.filter(status="Solved")
        return render(request, "reports/solved_crimes.html", {'solved_crimes': solved_crimes})


def UnderInvestigationCrimesReport(request):
    if request.POST:
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        searchResult = Crime.objects.filter(
            status="Under Investigation", updated_at__gte=from_date, updated_at__lte=to_date)
        download_form = DownloadForm(initial={
            'from_date': from_date,
            'to_date': to_date
        })
        return render(request, "reports/under_investigation_crimes.html", {'underInv_crimes': searchResult, 'download_form': download_form})
    else:
        underInv_crimes = Crime.objects.filter(status="Under Investigation")
        return render(request, "reports/under_investigation_crimes.html", {'underInv_crimes': underInv_crimes})


def downloadUnderInvestigation(request):
    if request.POST:
        form = DownloadForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=Crime under Inv' + \
                str(datetime.now())+'.pdf'
            response['Content-Transfer-Encoding'] = 'binary'

            crimes = Crime.objects.filter(
                status="Under Investigation", updated_at__gte=from_date, updated_at__lte=to_date)
            # render the html page
            html_string = render_to_string(
                'crimes/pdf_page.html', {'crimes': crimes})

            # transfort to html content
            html = HTML(string=html_string)
            result = html.write_pdf()

            # preview the content in the memory
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                # open the pdf and read it for reading
                output.seek(0)
                response.write(output.read())

            return response
        else:
            DownloadForm(request.POST)
    else:
        return redirect('under_inv_crimes')


def downloadSolved(request):
    if request.POST:
        form = DownloadForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=Crime under Inv' + \
                str(datetime.now())+'.pdf'
            response['Content-Transfer-Encoding'] = 'binary'

            crimes = Crime.objects.filter(
                status="Solved", updated_at__gte=from_date, updated_at__lte=to_date)
            # render the html page
            html_string = render_to_string(
                'crimes/pdf_page.html', {'crimes': crimes})

            # transfort to html content
            html = HTML(string=html_string)
            result = html.write_pdf()

            # preview the content in the memory
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                # open the pdf and read it for reading
                output.seek(0)
                response.write(output.read())

            return response
        else:
            DownloadForm(request.POST)
    else:
        return redirect('solved_crimes')


def downloadPending(request):
    if request.POST:
        form = DownloadForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=Crime under Inv' + \
                str(datetime.now())+'.pdf'
            response['Content-Transfer-Encoding'] = 'binary'

            crimes = Crime.objects.filter(
                status="Pending", updated_at__gte=from_date, updated_at__lte=to_date)
            # render the html page
            html_string = render_to_string(
                'crimes/pdf_page.html', {'crimes': crimes})

            # transfort to html content
            html = HTML(string=html_string)
            result = html.write_pdf()

            # preview the content in the memory
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                # open the pdf and read it for reading
                output.seek(0)
                response.write(output.read())

            return response
        else:
            DownloadForm(request.POST)
    else:
        return redirect('pending_crimes')


def DetectedCriminalReport(request):
    detectedCriminals = DetectedCriminal.objects.all()
    return render(request, 'reports/detectedCriminal.html', {'detectedCriminals': detectedCriminals})
