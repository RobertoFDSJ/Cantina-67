from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from produtos.models import Produto
from clientes.models import Cliente
from .models import Pedido
from django.db.models import Sum

# Função auxiliar para verificar grupos (Nomes exatos dos seus grupos)
def check_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@login_required
def adicionar_ao_carrinho(request, produto_id=None):
    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        qtd_adicionada = int(request.POST.get('quantidade', 1))
    else:
        qtd_adicionada = 1
    
    if not produto_id:
        messages.error(request, "Produto não selecionado.")
        return redirect('novo_pedido')

    carrinho = request.session.get('carrinho', {})
    p_id = str(produto_id)
    carrinho[p_id] = carrinho.get(p_id, 0) + qtd_adicionada
    request.session['carrinho'] = carrinho
    request.session.modified = True
    
    messages.success(request, f'Item adicionado ao carrinho!')
    return redirect('ver_carrinho')

def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    total_geral = 0
    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=produto_id)
        subtotal = produto.preco * quantidade
        total_geral += subtotal
        itens_carrinho.append({'produto': produto, 'quantidade': quantidade, 'subtotal': subtotal})
    return render(request, 'pedidos/carrinho.html', {'itens': itens_carrinho, 'total_geral': total_geral})

@login_required
def finalizar_compra(request):
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('home')

    # Busca o perfil do cliente vinculado ao usuário logado
    cliente_perfil = Cliente.objects.filter(usuario=request.user).first()
    
    if not cliente_perfil:
        # Se o usuário não tiver perfil, usa o primeiro como fallback para evitar erro de banco
        cliente_perfil = Cliente.objects.first()

    # Cria o pedido atrelando ao User logado
    pedido = Pedido.objects.create(
        usuario=request.user, 
        cliente=cliente_perfil, 
        pago=False
    )
    
    for produto_id in carrinho.keys():
        try:
            produto = Produto.objects.get(id=produto_id)
            pedido.produtos.add(produto)
        except Produto.DoesNotExist:
            continue
    
    request.session['carrinho'] = {}
    request.session.modified = True
    messages.success(request, "Pedido realizado com sucesso!")
    return redirect('lista_pedidos')

@login_required
def lista_pedidos(request):
    # Lógica de Permissão
    is_admin = request.user.is_superuser or check_group(request.user, 'Administradores')
    is_staff = request.user.is_staff or check_group(request.user, 'Funcionários')

    if is_admin or is_staff:
        # Equipe vê todos os pedidos
        pedidos = Pedido.objects.all().order_by('-data_pedido')
        
        # Filtro por nome do cliente (para funcionários/admins)
        nome_filtro = request.GET.get('cliente_nome')
        if nome_filtro:
            # Busca tanto no campo 'nome' do Cliente quanto no 'username' do User
            pedidos = pedidos.filter(cliente__nome__icontains=nome_filtro) | pedidos.filter(usuario__username__icontains=nome_filtro)
    else:
        # Clientes comuns veem apenas os próprios pedidos
        pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data_pedido')
    
    # Cálculo de faturamento e subtotais
    faturamento_total = 0
    for p in pedidos:
        total_pedido = p.produtos.aggregate(Sum('preco'))['preco__sum'] or 0
        p.total_calculado = total_pedido
        faturamento_total += total_pedido
        
    return render(request, 'pedidos/lista_pedidos.html', {
        'pedidos': pedidos, 
        'faturamento_total': faturamento_total
    })

@login_required
def excluir_pedido(request, pedido_id):
    # Proteção de exclusão: Apenas Administradores (Grupo ou Superusuário)
    if not (request.user.is_superuser or check_group(request.user, 'Administradores')):
        messages.error(request, "Acesso negado. Apenas administradores podem excluir pedidos.")
        return redirect('lista_pedidos')
        
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()
    messages.success(request, "Pedido removido com sucesso.")
    return redirect('lista_pedidos')

def limpar_carrinho(request):
    request.session['carrinho'] = {}
    request.session.modified = True
    return redirect('ver_carrinho')

@login_required
def novo_pedido(request):
    # Carrega dados para a tela de venda direta/novo pedido
    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    return render(request, 'pedidos/novo_pedido.html', {'clientes': clientes, 'produtos': produtos})

