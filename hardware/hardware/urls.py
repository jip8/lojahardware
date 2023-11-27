from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from loja.views import home, registrar, login, logout
from loja.views import admprodutos, rmv_prod, alt_prod
from loja.views import carrinho, adicionar_carrinho, remover_item


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('registrar/', registrar, name='registrar'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('admprodutos/', admprodutos, name='admprodutos'),
    path('rmv_prod/<int:produto_id>/', rmv_prod, name='rmv_prod'),
    path('alt_prod/<int:produto_id>/', alt_prod, name='alt_prod'),
    path('carrinho/', carrinho, name='carrinho'),
    path('adicionar_carrinho/<int:produto_id>/', adicionar_carrinho, name='adicionar_carrinho'),
    path('remover_item/<int:produto_id>/', remover_item, name='remover_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)