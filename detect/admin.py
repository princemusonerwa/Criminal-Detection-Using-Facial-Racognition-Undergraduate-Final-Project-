from django.contrib import admin
from .models import Crime, Student, Employee, Gallery, Faculty, Department

# Register your models here.
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Crime)
admin.site.register(Gallery)
admin.site.register(Faculty)
admin.site.register(Department)