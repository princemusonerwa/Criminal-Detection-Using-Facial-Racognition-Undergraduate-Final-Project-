from .models import Person, DetectedCriminal 
from django.core.mail import send_mail
from FaceRecognition.settings import EMAIL_HOST_USER
import datetime
import pytz
import requests

utc=pytz.UTC

def send_notify(id,location):
    splited_id=id.split("_")[0]
    person = Person.objects.get(id=splited_id)
    if person.status == 'W':
        latest = person.detectedcriminal_set.all().last()
        if (latest is None) or ((datetime.datetime.now().replace(tzinfo=utc)-latest.time).total_seconds()>60):
            DetectedCriminal.objects.create(person=person, location=location)
            message = ""
            if(hasattr(person,"student")): 
               message = f'Criminal(student) by names of {person.student.names} has been detected {location} in Auca premises.'             
            if(hasattr(person,"employee")): 
               message = f'Criminal(employee) by names of {person.employee.names} has been detected {location} in Auca premises.'
            send_sms(['0787882305'], message)
            send_mail_to('Detected', message ,['shemusopri@gmail.com','musonerwaprince@gmail.com'])
            
        
def send_mail_to(subject, message, receivers):
     # make sure receivers variable is an array
    send_mail(subject,message,EMAIL_HOST_USER,receivers, fail_silently= False)

def send_sms(phones,message):
    # make sure phones variable is an array
    data    =   {'recipients':','.join(phones),'message':message, 'sender':'+250787917010'}
    url     =   'https://www.intouchsms.co.rw/api/sendsms/.json'
    r       =   requests.post(url,data=data,auth=("shema19974","Prince@1997"))
    print (r.json(), r.status_code)

    




