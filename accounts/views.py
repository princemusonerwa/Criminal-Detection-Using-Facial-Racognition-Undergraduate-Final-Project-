from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileUpdateForm, UserUpdateForm
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