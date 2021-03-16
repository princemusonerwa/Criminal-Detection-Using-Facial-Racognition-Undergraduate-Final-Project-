"""FaceRecognition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', include('accounts.urls')),
    path('', views.home, name="home"),
    path('', include('detect.urls')),
    path('index', views.index, name="index"),
    path('person_status_summary', views.person_status_summary, name="person_status_summary"),
    path('person_gender_summary', views.person_gender_summary, name="person_gender_summary"),
    path('crime_status_summary', views.crime_status_summary, name="crime_status_summary"),
    path('admin/', admin.site.urls),
]

handler404 = 'FaceRecognition.views.error_404_view'
handler500 = 'FaceRecognition.views.error_500_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
