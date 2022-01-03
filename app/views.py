from django.shortcuts import render, HttpResponse, redirect, render

def home(request):

    return render(request,'home.html')

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def login_process(request):
    pass

def register_process(request):
    pass