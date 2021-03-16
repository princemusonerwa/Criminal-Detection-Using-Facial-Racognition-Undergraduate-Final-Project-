from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from detect.models import Student, Employee, Person, DetectedCriminal, Crime
from django.db.models import Count
from django.http import JsonResponse
import datetime

@login_required
def index(request):
    numberOfStudents = Student.objects.count()
    numberOfEmployees = Employee.objects.count()
    numberOfCriminals = Person.objects.filter(status = 'WANTED').count()
    numberOfPeople = Person.objects.count()
    people = Person.objects.all()
    detectedCriminal = DetectedCriminal.objects.all()

    context = {
        'numberOfStudents' : numberOfStudents,
        'numberOfEmployees' : numberOfEmployees,
        'numberOfCriminals' : numberOfCriminals,
        'numberOfPeople' : numberOfPeople,
        'people' : people,
        'detectedCriminal' : detectedCriminal,

    }
    return render(request, "index.html", context)

def home(request):
    crimes = Crime.objects.all().order_by('-updated_at')[:3]
    return render(request, "home.html", {'crimes':crimes})

def error_404_view(request, exception):
    return render(request,'404.html')

def error_500_view(request):
    return render(request,'500.html')

def person_status_summary(request):
    todays_date = datetime.date.today()
    six_months_age = todays_date - datetime.timedelta(days= 30*6)

    people = Person.objects.filter(updated_at__gte=six_months_age, updated_at__lte=todays_date)
    final_rep = {}

    def get_status(person):
        return person.status

    status_list = list(set(map(get_status, people)))

    def get_person_status_count(status):
        count = 0
        filtered_by_status = people.filter(status = status)
        for item in filtered_by_status:
            count+=1
        return count

    for x in people:
        for y in status_list:
            final_rep[y] = get_person_status_count(y)

    return JsonResponse({'person_status_data': final_rep}, safe=False )

def person_gender_summary(request):
    people = Person.objects.all()
    final_rep = {}

    def get_gender(person):
        return person.gender

    gender_list = list(set(map(get_gender, people)))

    def get_person_gender_count(gender):
        count = 0
        filtered_by_gender = people.filter(gender= gender)
        for item in filtered_by_gender:
            count+=1
        return count

    for x in people:
        for y in gender_list:
            final_rep[y] = get_person_gender_count(y)

    return JsonResponse({'person_gender_data': final_rep}, safe=False )

def crime_status_summary(request):
    todays_date = datetime.date.today()
    six_months_age = todays_date - datetime.timedelta(days= 30*6)

    crimes = Crime.objects.filter(updated_at__gte=six_months_age, updated_at__lte=todays_date)
    final_rep = {}

    def get_status(crime):
        return crime.status

    status_list = list(set(map(get_status, crimes)))

    def get_crime_status_count(status):
        count = 0
        filtered_by_status = crimes.filter(status = status)
        for item in filtered_by_status:
            count+=1
        return count

    for x in crimes:
        for y in status_list:
            final_rep[y] = get_crime_status_count(y)

    return JsonResponse({'crime_status_data': final_rep}, safe=False )