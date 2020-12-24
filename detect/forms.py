from django import forms
from .models import Student, Employee, Gallery, Crime, Department

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_id', 'names', 'email','phone', 'gender', 'dob', 'address', 'status', 'faculty', 'department')

        widgets = {
            'student_id' : forms.TextInput(attrs={'class': 'form-control'})
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
    class Meta:
        model = Employee
        fields = fields = ('staff_id', 'names', 'email','phone', 'gender', 'dob', 'address', 'status')

class GalleryForm(forms.ModelForm):
    photos = forms.ImageField(label='Photos')    
    class Meta:
        model = Gallery
        fields = ('photos', )

class CrimeForm(forms.ModelForm):
    class Meta:
        model = Crime
        fields = '__all__'