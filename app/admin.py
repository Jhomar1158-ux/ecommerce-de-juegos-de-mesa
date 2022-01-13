from django.contrib import admin
from app.models import *
# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    pass
admin.site.register(Users, UsersAdmin)

class ProductsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Products, ProductsAdmin)

class CategoriasAdmin(admin.ModelAdmin):
    pass
admin.site.register(Categorias, CategoriasAdmin)

class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile)

class OrdenAdmin (admin.ModelAdmin):
    pass
admin.site.register(Orden, OrdenAdmin)

class CantidadProductoAdmin (admin.ModelAdmin):
    pass
admin.site.register(CantidadProducto, CantidadProductoAdmin)