from django.urls import path
from . import views

urlpatterns = [
    path('student/create', views.addStudent, name='add_student'),
    path('student', views.allStudent, name='students'),
    path('student/<int:id>', views.studentDetails, name='student_details'),
    path('student/<int:id>/delete', views.deleteStudent, name='delete_student'),
    path('student/<int:id>/edit', views.updateStudent, name='edit_student'),

    path('image/<int:id>/create', views.addImage, name='add_image'),
    path('ajax/load-departments/', views.loadDepartments, name='ajax_load_departments'),
    path('image/<int:id>', views.deleteImage, name='delete_image'),

    path('employee/create', views.addEmployee, name='add_employee'),
    path('employee', views.allEmployee, name='employees'), 
    path('employee/<int:id>', views.employeeDetails, name='employee_details'),
    path('employee/<int:id>/delete', views.deleteEmployee, name='delete_employee'),
    path('employee/<int:id>/edit', views.updateEmployee, name='edit_employee'),

    path('crime/create', views.addCrime, name='add_crime'),
    path('crime', views.allCrime, name='crimes'),
    path('crime/<int:id>', views.crimeDetails, name='crime_details'),
    path('crime/<int:id>/delete', views.deleteCrime, name='delete_crime'),
    path('crime/<int:id>/edit', views.updateCrime, name='edit_crime'),

    path('faculty/create', views.addFaculty, name='add_faculty'),
    path('faculty', views.allFaculty, name='faculties'),
    path('faculty/<int:id>', views.facultyDetails, name='faculty_details'),
    path('faculty/<int:id>/delete', views.deleteFaculty, name='delete_faculty'),
    path('facutly/<int:id>/edit', views.updateFaculty, name='edit_faculty'),

    path('department/create', views.addDepartment, name='add_department'),
    path('department', views.allDepartment, name='departments'),
    path('department/<int:id>', views.departmentDetails, name='department_details'),
    path('department/<int:id>/delete', views.deleteDepartment, name='delete_department'),
    path('department/<int:id>/edit', views.updateDepartment, name='edit_department'),

    path('detect/', views.detect, name='detect'),
    path('train/', views.train_images, name='trainData'),

    path('image/', views.detect_image, name="imagedetection"),  
    path('camera/', views.detect_criminal, name='cameradetection'),

    path('export-student-csv', views.exportStudentListCsv, name='export_student_csv'),
    path('export-student-excel', views.exportStudentListexcel, name='export_student_excel'),
    path('export-student-pdf', views.exportStudentListPdf, name='export_student_pdf'),
    path('export-employee-csv', views.exportEmployeeListCsv, name='export_employee_csv'),
    path('export-employee-excel', views.exportEmployeeListExcel, name='export_employee_excel'),
    path('export-employee-pdf', views.exportEmployeeListPdf, name='export_employee_pdf'),
]