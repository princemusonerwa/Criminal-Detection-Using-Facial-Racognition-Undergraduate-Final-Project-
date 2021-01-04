from django import forms
from .models import Student, Employee, Gallery, Crime, Department

class StudentForm(forms.ModelForm):
    CHOICES = (('NOT WANTED', 'NOT WANTED'),('WANTED', 'WANTED'),)
    status = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Student
        fields = ('student_id', 'names', 'email','phone', 'gender', 'dob', 'address', 'status', 'faculty', 'department')

        widgets = {
            'student_id' : forms.TextInput(attrs={'class': 'form-control'}),
            'names' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'phone' : forms.TextInput(attrs={'class': 'form-control'}),
            'gender' : forms.TextInput(attrs={'class': 'form-control'}),
            'dob' : forms.TextInput(attrs={'class': 'form-control'}),
            'faculty' : forms.Select(attrs={'class': 'form-control'}),
            'department' : forms.Select(attrs={'class': 'form-control'}),
            'address' : forms.TextInput(attrs={'class': 'form-control'}),         
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.none()

        if 'faculty' in self.data:
            try:
                faculty_id = int(self.data.get('faculty'))
                self.fields['department'].queryset = Department.objects.filter(faculty_id=faculty_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.faculty.department_set.order_by('name')

        
class EmployeeForm(forms.ModelForm):
    CHOICES = (('NOT WANTED', 'NOT WANTED'),('WANTED', 'WANTED'),)
    status = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Employee
        fields = fields = ('staff_id', 'names', 'email','phone', 'gender', 'dob', 'address', 'status')

        widgets = {
            'staff_id' : forms.TextInput(attrs={'class': 'form-control'}),
            'names' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'phone' : forms.TextInput(attrs={'class': 'form-control'}),
            'gender' : forms.TextInput(attrs={'class': 'form-control'}),
            'dob' : forms.TextInput(attrs={'class': 'form-control'}),
            'address' : forms.TextInput(attrs={'class': 'form-control'}),         
        }

class GalleryForm(forms.ModelForm):
    photos = forms.ImageField(label='Photos')    
    class Meta:
        model = Gallery
        fields = ('photos', )

class CrimeForm(forms.ModelForm):
    class Meta:
        model = Crime
        fields = '__all__'