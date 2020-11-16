from django import forms
from .models import Student, Employee, Gallery, Crime

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class GalleryForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Gallery
        fields = ('image', )

class CrimeForm(forms.ModelForm):
    class Meta:
        model = Crime
        fields = '__all__'