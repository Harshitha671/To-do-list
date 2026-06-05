from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'signup.html',
                {'error': 'Username already exists'}
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(request, 'signup.html')

def login_user(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/')

        return render(
            request,
            'login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/login/')