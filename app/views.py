from django.shortcuts import render, HttpResponse, redirect, render
from app.models import *
from django.contrib import messages
from django.core import serializers
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

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
    if id==0:
        return redirect('/login')
    else:
        user_profile=Users.objects.get(id=id)
        print('user_profile.profile.image.url')
        context={
            'user_profile':user_profile,
        }
        return render(request,'profile.html',context)
    
def newsletter(request):
    mail=request.POST['email']
    print(mail)
    mailcheck=Newsletter_users.objects.filter(correo=mail)
    if mailcheck:
        print('Este correo ya está registrado.')
        return redirect('/')
    else:
        print('Guardando correo.')
        Newsletter_users.objects.create(correo=mail)
        request.session['u_newsletter']=mail
        ###################### TRABAJANDO ############################
        context={
            'mail': mail,
        }

        template=get_template('newsletter.html')
        content= template.render(context)

        email=EmailMultiAlternatives(
            '¡Enhorabuena, te has registrado correctamente a nuestro Newsletter!',
            'Juegos de Mesa - Juégalo',
            settings.EMAIL_HOST_USER,
            [mail]
        )
        email.attach_alternative(content, 'text/html')
        email.send()
        return redirect('/newsletter_confirm')
    

def newsletter_confirm(request):
    return render(request, 'newsletter_confirm.html')

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

def producto(request,id):
    producto= Products.objects.get(id=id)
    context={
        "producto": producto
    }
    return render(request,'producto.html', context)

# def carrito(request):
#     pedido = request.POST["pedido"]
#     u = Users.objects.filter( id=request.session['u_id']) 
#     p=Products.objects.filter(nombre = pedido)
#     if p.stock > 0:
#         # orden = Orden.objects.filter(u) recibir Orden del Usuario que tiene "finalizado" = falso 
#         # si filter regresa una lista vacia orden no existe / se creara otra orden para el usuario y se agregara p a prodructo 
#         # si filter regresa una lista con un orden adentro se agregara p a la lista de orden 
#         # (else) se agregara un mesaje que diga que ya no hay cambios y se redireccionara a la vista del carrito

#         print("encontrado")
#         print(p)
#     return redirect('/')


def search(request):
    var_searched=request.POST['search']
    var_result=Products.objects.filter(nombre__contains=var_searched)
    context={
        'products':var_result,
    }
    return render(request, 'home.html', context)

def categorias(request, tipo):
    if tipo=='TOD':

        context={
            'tipo':"TODOS LOS JUEGOS",
            'products':Products.objects.all(),
        }
        return render(request, 'categorias.html' , context)
    else:
        result_tod=Products.objects.filter(category_slug__contains=tipo)
        print(result_tod)
        if tipo=='FAM':
            tipo='FAMILIA'
        elif tipo=='INF':
            tipo='INFANTILES'
        elif tipo=='NAP':
            tipo='NAIPES'
        context={
            'tipo':tipo,
            'products': result_tod,
        }
        return render(request, 'categorias.html' , context )

def carrito(request):
    print("sesion1",request.session.get('u_id'))
    if request.session.get('u_id')== 0:
        #if request.session.get('u_id')== none: 
        print("AQUI ESTA")
        return redirect('/login')
    pedido = request.POST["pedido"]
    u = Users.objects.get( id=request.session['u_id']) 
    p=Products.objects.filter(nombre = pedido)
    # agragar al models de producto cantidad para que a agregar al carrito sumar las cantidades de ese producto (preguntar hoy)
    print(u,"USUARIO")
    
    if p[0].stock > 0:
        # orden = Orden.objects.filter(usuario = u ).filter(finalizado = False) #recibir Orden del Usuario que tiene "finalizado" = falso 
        orden = Orden.objects.filter(usuario = u, finalizado = False )
        print("stock mas de 0")
        print(orden)
        if orden:
            print("se encontro un orden")
            orden = orden[0]
            producto = orden.cantidad_productos.all()
            cantidad = producto.filter(producto=p[0])
            if cantidad :
                cantidad[0].cantidad = cantidad[0].cantidad +1
                cantidad[0].save()
            else:
                new_cantidad_producto = CantidadProducto.objects.create(cantidad = 1, producto = p[0])
                orden.cantidad_productos.add(new_cantidad_producto)
            orden.save()
            total = 0 
            for i in orden.cantidad_productos.all():
                total = total + i.cantidad
                print(i.cantidad)
            print(producto.filter(producto=p[0])[0].cantidad)
            request.session["orden"]= total
            
            # orden_si = Orden.objects.create(usuario = u)
            # orden.producto.add(p[0])
            # request.session["orden"]= orden.producto.all().count()
        #     orden[0].producto.all.add(p) # si filter regresa una lista vacia orden no existe / se creara otra orden para el usuario y se agregara p a prodructo 
        # # si filter regresa una lista con un orden adentro se agregara p a la lista de orden 
        else:
            print("no se encontro ningun orden")
            new_orden = Orden.objects.create(usuario = u)
            print(new_orden)
            new_cantidad_producto = CantidadProducto.objects.create(cantidad = 1, producto = p[0])
            new_orden.cantidad_productos.add(new_cantidad_producto)
            print(new_orden)
            request.session["orden"]= new_orden.cantidad_productos.all().count()
        #     Orden.objects.create(producto= pedido, usuario = u)
        #     print("No se realizaron cambios")
        #     return render(request,'carrito.html')# (else) se agregara un mesaje que diga que ya no hay cambios y se redireccionara a la vista del carrito

        print("encontrado")
        
        print(p)
    else:
        print ("stock insuficiente")
    return redirect('/resumen')

def carrito_resumen(request):
    u = Users.objects.get( id=request.session['u_id'])
    # pedido = request.POST["pedido"]
    # producto=Products.objects.filter(nombre = pedido)
    orden = Orden.objects.filter(usuario = u,finalizado = False)
    print(orden[0])

    context = {
        "orden": orden[0],
    }
    # for i in orden[0].cantidad_productos.all():
    #     print(i.producto)

    return render(request, 'carrito.html', context)



def eliminarProducto (request):
    u = Users.objects.get( id=request.session['u_id']) 
    # o = request.POST["orden"]
    p = request.POST["producto"]

    orden = Orden.objects.filter(usuario = u, finalizado = False )
    if orden:
        orden = orden[0]
        pc = orden.cantidad_productos.all().filter(producto = p)
        orden.cantidad_productos.remove(pc)
        orden.save()
        # crear un if preguntando si es todo o uno solo 
    return redirect('/')
