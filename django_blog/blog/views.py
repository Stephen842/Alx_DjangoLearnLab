from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm


# Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'Django Blog - Register Now'
    }
    return render(request, 'blog/register.html', context)

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('home')
            
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'title': '',
    }
    return render(request, 'blog/login.html', context)

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')

# Landing page view
def home(request):
    context = {
        'title': '',
    }
    return render(request, 'blog/home.html', context)

# Profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
    return render(request, 'blog/profile.html')