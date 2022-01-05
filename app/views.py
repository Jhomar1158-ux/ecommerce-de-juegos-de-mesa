from django.shortcuts import render, HttpResponse, redirect, render
from app.models import *

def home(request):
    context={
        "products": Products.objects.all()
    }
    return render(request,'home.html', context)

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

# def producto (request):
#     context = {}
#     tamaño = "pequeño,mediano,grande"
#     tamaño = tamaño.split(',')

#     if nombre == "ramos":
#         producto= Producto.objects.get(id=1)
#         print(producto)
#         producto.tamaño=producto.tamaño.split(',')
#         producto.precio=producto.precio.split(',')
#         row=[]
#         for i in range (len(producto.tamaño)):
#             row.append({"tamaño":producto.tamaño[i],"precio":producto.precio[i]})
#         context={
#             "producto":producto,
#             "row":row,
#             "range":range(1,5),
#         }