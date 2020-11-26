from django.urls import path
from . import views

urlpatterns = [
    path('student/create', views.addStudent, name='add_student'),
    path('student', views.allStudent, name='students'),
    path('student/<int:id>', views.studentDetails, name='student_details'),
    path('student/<int:id>/delete', views.deleteStudent, name='delete_student'),
    path('student/<int:id>/edit', views.updateStudent, name='edit_student'),
    path('student/<int:id>/image/<int:image_pk>/delete', views.deleteStudentImage, name='delete_student_image'),
    path('student/image/<int:id>/create', views.addStudentImage, name='add_student_image'),
    path('ajax/load-departments/', views.loadDepartments, name='ajax_load_departments'),
    path('employee/create', views.addEmployee, name='add_employee'),
    path('employee', views.allEmployee, name='employees'),
    path('employee/<int:id>', views.employeeDetails, name='employee_details'),
    path('employee/<int:id>/delete', views.deleteEmployee, name='delete_employee'),
    path('employee/<int:id>/edit', views.updateEmployee, name='edit_employee'),
    path('employee/<int:id>/image/<int:image_pk>/delete', views.deleteEmployeeImage, name='delete_employee_image'),
    path('employee/image/<int:id>/create', views.addEmployeeImage, name='add_employee_image'),
    path('crime/create', views.addCrime, name='add_crime'),
    path('crime', views.allCrime, name='crimes'),
    path('crime/<int:id>', views.crimeDetails, name='crime_details'),
    path('crime/<int:id>/delete', views.deleteCrime, name='delete_crime'),
    path('crime/<int:id>/edit', views.updateCrime, name='edit_crime'),
    path('train/', views.train_images, name='trainData'),
    path('detect/', views.detect_criminal, name='webcamdetection'),
    path('image/', views.detect_image, name="imagedetection"),   

]