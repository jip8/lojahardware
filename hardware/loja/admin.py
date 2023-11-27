from django.contrib import admin
from .models import Usuario, Cart, Produto, ComponenteHardware, Periferico

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'estoque']

@admin.register(ComponenteHardware)
class ComponenteHardwareAdmin(admin.ModelAdmin):
    pass

@admin.register(Periferico)
class PerifericoAdmin(admin.ModelAdmin):
    pass
