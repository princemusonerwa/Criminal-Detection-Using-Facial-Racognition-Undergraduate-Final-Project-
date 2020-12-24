from django.db import models
import uuid
from PIL import Image
from datetime import datetime

# Create your models

def get_upload_to(instance,filename):
    new_filename= '{}.{}'.format(uuid.uuid4(),filename.split('.')[-1])
    folder=""
    if(hasattr(instance.person,"student")):
        folder=f"{instance.person.id}_{instance.person.names}_student_{instance.person.student.student_id}"
    elif(hasattr(instance.person,"employee")):
        folder=f"{instance.person.id}_{instance.person.names}_employee_{instance.person.employee.staff_id}"

    return "images/training/{}/{}".format(folder,new_filename)

class Person(models.Model):
    names = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', unique=True)
    phone = models.CharField(verbose_name="Phone Number", max_length=15)
    gender = models.CharField(max_length=255)
    dob = models.DateField(verbose_name="Date of Birth", null="True")
    address = models.CharField(max_length=255)
    STATUS_CHOICES = [
      ('NT', 'NOT WANTED'),
      ('W', 'WANTED')
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="NOT WANTED")


class Faculty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(Person):
    student_id = models.IntegerField(primary_key = True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.names

class Employee(Person):
    staff_id = models.IntegerField(primary_key = True)

    def __str__(self):
        self.name


class Gallery(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    photos = models.ImageField(upload_to = get_upload_to)
    
class Crime(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255)
    description = models.TextField()
    STATUS_CHOICES = [
        ('UI', 'Under Investigation'),
        ('SO', 'Solved'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Under Investigation")

    def __str__(self):
        return self.person.names


class DetectedCriminal(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, default=None)
    time = models.DateTimeField(default = datetime.now, blank= True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.person.names




        
        



