from django.urls import path
from . import views

urlpatterns = [
    # Rota da Home (se houver)
    path('', views.home, name='home'),
    
    # Rota do Cardápio - ESSA É A QUE ESTÁ DANDO ERRO
    path('cardapio/', views.cardapio, name='cardapio'),
]