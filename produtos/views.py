from django.shortcuts import render
from .models import Produto

def home(request):
    # Filtra apenas o que está disponível e embaralha a ordem
    salgados = Produto.objects.filter(disponivel=True).order_by('?')[:6]
    return render(request, 'produtos/home.html', {'salgados': salgados})

def cardapio(request):
    # Busca todos os produtos para exibir ao público
    produtos = Produto.objects.all().order_by('nome')
    return render(request, 'produtos/cardapio.html', {'produtos': produtos})