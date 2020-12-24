from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.
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
    return render(request, 'accounts/register.html', {'form': form})

def allUsers(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users':users})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
