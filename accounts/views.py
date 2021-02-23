from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserForm, ProfileUpdateForm, UserUpdateForm, MyAuthenticationForm, ReporterForm
from .models import User
from django.contrib import messages
from datetime import datetime
from functools import wraps
from django.core.exceptions import PermissionDenied
from io import BytesIO
import csv
import xlwt
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def check_is_admin(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_admin == False:
            raise PermissionDenied()
        return func(request, *args, **kwargs)
    return wrapper

@login_required
@check_is_admin
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data.get('names')
            form.save()
            messages.success(request, f'Account created for {names}!')
            return redirect('users')
    else:
        form = UserForm()
    return render(request, 'accounts/add_user.html', {'form': form})

def addReporter(request):
	if request.method == "POST":
		form = ReporterForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, "Registration successful." )
			return redirect("signin")
	else:
	    form = ReporterForm
	return render (request, "accounts/register.html", {"form":form})


def updateUser(request, id):
    obj = get_object_or_404(User, id = id) 
    # pass the object as instance in form 
    form = UserForm(request.POST or None, instance = obj) 
    if form.is_valid():
        names = form.cleaned_data.get('names')
        form.save()
        messages.success(request, f'Account created for {names}!')
        return redirect('users')
    return render(request, 'accounts/register.html', {'form': form})

def deleteUser(request, id):
    user = User.objects.get(id = id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted Successfully.')
        return redirect('users')
    return render(request, 'accounts/user_confirm_delete.html', {'user':user})

@login_required
@check_is_admin
def allUsers(request):
    users = User.objects.filter(is_securityOfficer='True', is_admin='False')
    return render(request, 'accounts/user_list.html', {'users':users})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST or None, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST or None, request.FILES, instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(request.POST or None, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance = request.user.profile)
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form
    }
    return render(request, 'accounts/profile.html', context)

def signIn(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect('index')
        else:
            messages.error(request, "Email or password is invalid")
            return redirect('signin')
    else:
        form = MyAuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

def signOut(request):
    logout(request)
    return redirect('signin')

def exportUserListCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']= 'attachement; filename=UserList'+ str(datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['names', 'email', 'phone Number', 'Address', 'Gender'])
    users = User.objects.all()
    for user in users:
        writer.writerow([user.names, user.email, user.phone, user.address, user.gender])
    return response

def exportUserListPdf(request):
    path = "accounts/pdf_page.html"
    users = User.objects.all()
    context = {"users" : users}

    html = render_to_string(path,context)
    io_bytes = BytesIO()
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
    if not pdf.err:
        # we can just return the HttpResponse
        response = HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
        response['Content-Disposition']= 'inline; filename=UserList'+ str(datetime.now())+'.pdf'
        return response
    else:
        return HttpResponse("Error while rendering PDF", status=400)

def exportUserListExcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']= 'attachement; filename=UserList'+ str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['names', 'email', 'phone Number', 'Address', 'Gender']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = User.objects.all().values_list('names', 'email', 'phone', 'address', 'gender')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
        
    wb.save(response)

    return response