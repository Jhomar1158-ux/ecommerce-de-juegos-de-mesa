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

