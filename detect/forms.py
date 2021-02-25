from django import forms
from .models import Student, Employee, Gallery, Crime, Department, Person, Faculty, Department


class StudentForm(forms.ModelForm):
    student_id = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    names = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    GENDER_CHOICE = (('Male', 'Male'), ('Female', 'Female'))
    gender = forms.ChoiceField(choices=GENDER_CHOICE, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input  d-inline'}))
    dob = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    CHOICES = (('NOT WANTED', 'NOT WANTED'), ('WANTED', 'WANTED'),)
    status = forms.ChoiceField(
        choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    faculty = forms.Select(attrs={'class': 'form-control'})
    department = forms.Select(attrs={'class': 'form-control'})

    class Meta:
        model = Student
        fields = ('student_id', 'names', 'email', 'phone', 'gender',
                  'dob', 'address', 'status', 'faculty', 'department')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.none()

        if 'faculty' in self.data:
            try:
                faculty_id = int(self.data.get('faculty'))
                self.fields['department'].queryset = Department.objects.filter(
                    faculty_id=faculty_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.faculty.department_set.order_by(
                'name')


class EmployeeForm(forms.ModelForm):
    staff_id = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    names = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    GENDER_CHOICE = (('Male', 'Male'), ('Female', 'Female'))
    gender = forms.ChoiceField(choices=GENDER_CHOICE, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input  d-inline'}))
    dob = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    CHOICES = (('NOT WANTED', 'NOT WANTED'), ('WANTED', 'WANTED'),)
    status = forms.ChoiceField(
        choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = Employee
        fields = ('staff_id', 'names', 'email',
                  'phone', 'gender', 'dob', 'address', 'status')


class GalleryForm(forms.ModelForm):
    photos = forms.ImageField(label='Photos')

    class Meta:
        model = Gallery
        fields = ('photos', )

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty 
        fields = '__all__'

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department 
        fields = '__all__'

class CrimeForm(forms.ModelForm):
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    class Meta:
        model = Crime
        exclude = ['user', 'status']
