from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout   #login maintains sessions
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login/")
def passw(request):
    return render(request, 'index.html')

@login_required(login_url="/login/")
def saved_passwords(request):
    queryset = userAccount.objects.filter(user = request.user)
    # queryset = userAccount.objects.all()
    
    if request.GET.get('search'):
        queryset = queryset.filter(name_service__icontains = request.GET.get('search'))

    context = {'useraccs':queryset}
    return render(request, 'saved.html', context)

@login_required(login_url="/login/")
def add_account(request):
    if request.method == "POST":
        data = request.POST

        name_service = data.get('name_service')
        username_service = data.get('username_service')
        password_service = data.get('password_service')

        userAccount.objects.create(
            user = request.user,
            name_service = name_service,
            username_service = username_service,
            password_service = password_service
        )

        return redirect('/saved')
    
    return render(request, 'add.html')

def delete_acc(request, id):
    queryset = userAccount.objects.get(id=id)
    queryset.delete()
    return redirect('/saved')

def update_acc(request, id):
    queryset = userAccount.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        name_service = data.get('name_service')
        username_service = data.get('username_service')
        password_service = data.get('password_service')

        queryset.name_service = name_service
        queryset.username_service = username_service
        queryset.password_service = password_service

        queryset.save()

        return redirect('/saved')

    context = {'userAccs': queryset}

    return render(request, 'update_acc.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username = username).exists():
            messages.info(request, "Invalid Username")
            return redirect("/login/")
        
        user = authenticate(username = username, password = password)
        if user is None:
            messages.info(request, "Invalid Password")
            return redirect("/login/")
        else:
            login(request, user)
            return redirect("/")
        
    return render(request, 'login_page.html')

def logout_page(request):
    logout(request)
    return redirect("/login/")

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username already exists.")
            return redirect("/register/")

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
        )

        user.set_password(password) #predefined method in django to encrypt and save password
        user.save()
        # messages.info(request, "Account created successfully!")
        return redirect('/login/')

    return render(request, 'register.html')