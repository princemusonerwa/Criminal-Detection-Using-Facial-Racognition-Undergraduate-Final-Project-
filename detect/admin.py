from django.contrib import admin
from .models import Crime, Student, Employee, Images, Faculty, Department, DetectedCriminal

# Register your models here.
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Crime)
admin.site.register(Images)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(DetectedCriminal)