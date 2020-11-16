from django.db import models
import uuid

# Create your models

def get_upload_to(instance,filename):
    new_filename= '{}.{}'.format(uuid.uuid4(),filename.split('.')[-1])
    folder=""
    if(hasattr(instance.person,"student")):
        folder=f"{instance.person.id}_{instance.person.name}_student_{instance.person.student.student_id}"
    elif(hasattr(instance.person,"employee")):
        folder=f"{instance.person.id}_{instance.person.name}_employee_{instance.person.employee.staff_id}"

    return "images/training/{}/{}".format(folder,new_filename)

class Person(models.Model):
    names = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=255)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    STATUS_CHOICES = [
      ('NT', 'NOT WANTED'),
      ('W', 'WANTED')
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="NOT WANTED")


class Student(Person):
    student_id = models.IntegerField(primary_key = True)
    FACULTY_CHOICES = [
      ('BA', 'Business Administration'),
      ('ED', 'Education'),
      ('T', 'Theology'),
      ('IT', 'Information Technology'),
    ]
    faculty = models.CharField(max_length=100, choices=FACULTY_CHOICES)
    department = models.CharField(max_length=100)


class Employee(Person):
    staff_id = models.CharField(max_length=255)

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
      ('SO', 'Solved'),
      ('UI', 'Under Investigation'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Under Investigation")



        
        



