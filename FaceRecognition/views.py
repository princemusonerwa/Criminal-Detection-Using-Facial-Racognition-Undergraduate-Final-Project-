from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from detect.models import Student, Employee, Person

@login_required
def index(request):
    numberOfStudents = Student.objects.count()
    numberOfEmployees = Employee.objects.count()
    numberOfCriminals = Person.objects.filter(status = 'WANTED').count()
    numberOfPeople = Person.objects.count()
    people = Person.objects.all()
    context = {
        'numberOfStudents' : numberOfStudents,
        'numberOfEmployees' : numberOfEmployees,
        'numberOfCriminals' : numberOfCriminals,
        'numberOfPeople' : numberOfPeople,
        'people' : people,
    }
    return render(request, "index.html", context)