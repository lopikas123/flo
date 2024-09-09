from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, LoginForm

@login_required
def home(request):
    return render(request, 'home.html', {'username': request.user.username})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш аккаунт был создан')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя или пароль')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')