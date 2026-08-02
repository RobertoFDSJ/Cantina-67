from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from produtos.views import home 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('clientes/', include('clientes.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('', include('produtos.urls')),
    # Rota para autenticação (Login, Logout, Password Reset)
    path('accounts/', include('django.contrib.auth.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)