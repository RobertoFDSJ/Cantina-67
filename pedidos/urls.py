from django.urls import path
from . import views

urlpatterns = [
    path('relatorio/', views.lista_pedidos, name='lista_pedidos'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/limpar/', views.limpar_carrinho, name='limpar_carrinho'),
    path('carrinho/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('novo/', views.novo_pedido, name='novo_pedido'),
    
    # Rota para cliques na HOME (com ID)
    path('carrinho/add/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    
    # Rota para o formulário (sem ID na URL)
    path('carrinho/adicionar/', views.adicionar_ao_carrinho, name='adicionar_via_post'),

    # --- ROTA QUE ESTAVA FALTANDO ---
    # Esta linha permite que o botão de excluir no template funcione
    path('excluir/<int:pedido_id>/', views.excluir_pedido, name='excluir_pedido'),
]