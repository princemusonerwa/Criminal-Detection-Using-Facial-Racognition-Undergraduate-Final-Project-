from django import forms
from .models import Student, Employee, Gallery, Crime, Department, Person, Faculty, Department


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_id', 'names', 'email', 'phone', 'gender',
                  'dob', 'address', 'status', 'student_status','faculty', 'department')

        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'names': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.RadioSelect(attrs={'class': 'custom-radio-list'}),
            'dob': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'student_status': forms.Select(attrs={'class': 'form-control'})
        }

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
    class Meta:
        model = Employee
        fields = ('staff_id', 'names', 'email',
                  'phone', 'gender', 'dob', 'address', 'employee_status', 'status')
        widgets = {
            'staff_id': forms.TextInput(attrs={'class': 'form-control'}),
            'names': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'rows': 4, 'cols': 15}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.RadioSelect(attrs={'class': 'custom-radio-list'}),
            'dob': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_status': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

        def get_form(self, request, obj=None, **kwargs):
            if obj:
                if obj.get_profile().type==1:
                    self.exclude = ('user_permissions',)
            return super(EmployeeForm, self).get_form(request, obj=None, **kwargs)

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
    STATUS_CHOICES = [
        ('Under Investigation' , 'Under Investigation'),
        ('Solved' , 'Solved'),

    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial="Under Investigation")

    class Meta:
        model = Crime        
        fields = ('name','description','start_time','end_time','room','status')
        
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }

class DownloadForm(forms.Form):
    from_date = forms.CharField(widget=forms.HiddenInput)
    to_date = forms.CharField(widget=forms.HiddenInput)