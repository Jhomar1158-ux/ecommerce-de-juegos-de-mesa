from django.shortcuts import render, HttpResponse, redirect, render
from app.models import *
from django.contrib import messages
from django.core import serializers

import re
import bcrypt


def home(request):
    if 'login' not in request.session:
        request.session['login'] = False
    
    if 'u_id' not in request.session:
        request.session['u_id'] = 0
    context={
        "products": Products.objects.all()
    }
    return render(request,'home.html', context)

def register(request):
    return render(request,'register.html')

def register_process(request):
    check = Users.objects.filter(correo = request.POST['correo'])

    error = False
    
    if len(request.POST['nombre'])< 3:
        messages.error(request,'Tu nombre debe tener al menos 3 carácteres.', extra_tags = 'fn_error' )
        error = True

    if len(request.POST['apellido'])< 3:
        messages.error(request,'Tu apellido debe tener al menos 3 carácteres.', extra_tags = 'ln_error')
        error = True
    
    if check:
        messages.error(request,'Este email ya se encuentra registrado', extra_tags = 'email_error')
        error = True

    # PASSWORD, CONFIRM PASSWORD 

    if request.POST['password'] != request.POST['confirm_password']:
        messages.error(request,'Las contraseñas no coinciden', extra_tags = 'pw_error')
        error = True

    if len(request.POST['password']) < 8 :
        messages.error(request,'Tu contraseña debe teener al menos 8 carácteres', extra_tags = 'pw_error')
        error = True

    # =======================================

    if error == True:
        return redirect('/register')

    elif error == False:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = Users.objects.create(nombre = request.POST['nombre'], apellido = request.POST['apellido'],correo=request.POST['correo'], password = pw_hash)
        print(new_user)
        Profile.objects.create(user=new_user)
        request.session['user_id'] = new_user.id
        return redirect("/login")

def login(request):
    return render(request,'login.html')

def login_process(request):
    email = request.POST["correo"]
    password = request.POST["password"]
    print(f"{email} {password}")
    echeck = Users.objects.filter(correo=email) 
    print (echeck)
    if echeck:
        print('EXISTE EMAIL')
        if bcrypt.checkpw(password.encode(), echeck[0].password.encode()):
            print(echeck[0].password)
            request.session['login'] = True
            request.session['u_id'] = echeck[0].id
            # =======================MODIFICANDO=========================
            return redirect('/home_login')
        else:
            print('CONTRASEÑA INCORRECTA')
            messages.error(request,'Contraseña incorrecta', extra_tags = 'mal_login_pass_dato')
            return redirect('/login')
    else: 
        messages.error(request,'Email No registrado', extra_tags = 'mal_dato_login_e')
        return redirect('/login')

def home_login(request):
    print('INGRESO AL DASHBOARD FRIENDS')
    if request.session['login'] == True:
        user_1 = Users.objects.get(id = request.session['u_id'])
        context={
            'products':Products.objects.all(),
            'user': user_1,
        }
        return render(request, 'home_login.html', context)
    else:
        return redirect('/')

def profile(request,id):
    user_profile=Users.objects.get(id=id)
    print('user_profile.profile.image.url')
    context={
        'user_profile':user_profile,
    }
    return render(request,'profile.html',context)
    



def logout(request):
    request.session.clear()
    return redirect('/')





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