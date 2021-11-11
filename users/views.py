from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


def register(request):

    new_user = RegisterForm(request.POST or None)

    if request.method == 'POST':
        new_user = RegisterForm(request.POST)
        if new_user.is_valid():
            new_user = new_user.save()
            messages.success(request, 'Account was created for ' + new_user.username)
            return redirect('users:movies_login')

    context = {'form': new_user}
    return render(request, 'register.html', context)


def movies_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('movies:search')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {'form': form}
    return render(request, 'login.html', context)


def movies_logout(request):
    logout(request)
    return redirect('users:movies_login')
