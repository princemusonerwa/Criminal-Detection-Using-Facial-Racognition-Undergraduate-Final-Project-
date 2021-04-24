from django.db import models
from datetime import date
import uuid
from PIL import Image
from datetime import datetime
from django.core.exceptions import ValidationError
import re
from django.core.validators import MinLengthValidator
from django.conf import settings


# Create your models

def get_upload_to(instance, filename):
    new_filename = '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1])
    folder = ""
    if(hasattr(instance.person, "student")):
        folder = f"{instance.person.id}_{instance.person.names}_student_{instance.person.student.student_id}"
    elif(hasattr(instance.person, "employee")):
        folder = f"{instance.person.id}_{instance.person.names}_employee_{instance.person.employee.staff_id}"

    return "images/training/{}/{}".format(folder, new_filename)


def validate_mobile(value):
    """ Raise a ValidationError if the value looks like a mobile telephone number.
    """
    rule = re.compile(r'^07[238]\d{7}$')

    if not rule.search(value):
        msg = u"Invalid mobile number. Phone must be made with 07 followed by 2,3,8 which is also followed by 7 numbers."
        raise ValidationError(msg)


def validate_dob(value):
    today = date.today()
    if today < value:
        raise ValidationError('Date of birth cannot be in future.')


def validate_names(value):
    if len(value) < 5 and not value in int:
        raise ValidationError("Names should have atleast 5 characters")


class Person(models.Model):
    names = models.CharField(max_length=255, validators=[validate_names])
    email = models.EmailField(verbose_name='email address', unique=True)
    phone = models.CharField(verbose_name="Phone Number",
                             max_length=15, validators=[validate_mobile])
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(
        max_length=255, choices=GENDER_CHOICES, default="Male")
    dob = models.DateField(verbose_name="Date of Birth",
                           null="True", validators=[validate_dob])
    address = models.CharField(max_length=255)
    updated_at = models.DateField(auto_now=True)
    STATUS_CHOICES = [
        ('Not Wanted', 'Not Wanted'),
        ('Wanted', 'Wanted')
    ]
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="Not Wanted")

    def __str__(self):
        return self.names


class Faculty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def validate_length(value):
    value = str(value)
    if not len(value) == 5:
        raise ValidationError("Id must be made of 5 digits")


class Student(Person):
    student_id = models.IntegerField(
        primary_key=True, validators=[validate_length])
    STUDENT_STATUS = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Graduated', 'Graduated'),
        ('Suspended', 'Suspended')
    ]
    student_status = models.CharField(
        max_length=100, choices=STUDENT_STATUS, default="Active")
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.names


class Employee(Person):
    staff_id = models.IntegerField(primary_key=True)
    DEPARTMENT_CHOICES = [
        ('Human Resource', 'Human Resource'),
        ('Finance', 'Finance'),
        ('Information Management', 'Information Management'),
        ('Administration', 'Administration'),
    ]
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    EMPLOYEE_STATUS = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Fired', 'Fired'),
    ]
    employee_status = models.CharField(
        max_length=100, choices=EMPLOYEE_STATUS, default="Active")

    def __str__(self):
        self.name


class Images(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    photos = models.ImageField(upload_to=get_upload_to)


class Crime(models.Model):
    victim = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="crime_victim")
    CRIME_CHOICE = [
        ('Phone Robbery', 'Phone Robbery'),
        ('Cabble Robbery', 'Cabble Robbery'),
        ('Computer Robbery', 'Computer Robbery'),
    ]
    crime_type = models.CharField(
        max_length=100, choices=CRIME_CHOICE, default="Phone robbery")
    description = models.TextField()
    updated_at = models.DateField(auto_now=True)
    room = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Investigation', 'Under Investigation'),
        ('Solved', 'Solved'),
    ]
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="Pending",)
    suspect = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="crime_suspect", null=True)
    comment = models.TextField(max_length=255, null=True)

    def __str__(self):
        return self.crime_type


class DetectedCriminal(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, default=None)
    time = models.DateTimeField(default=datetime.now, blank=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.person.names
