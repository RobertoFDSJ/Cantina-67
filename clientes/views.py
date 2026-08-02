from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Cliente

def cadastrar_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('password')

        if Cliente.objects.filter(cpf=cpf).exists():
            messages.error(request, 'Este CPF já está cadastrado.')
            return render(request, 'clientes/cadastro.html')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Este e-mail já está em uso.')
            return render(request, 'clientes/cadastro.html')

        try:
            # 1. Cria o Usuário com o nome no first_name para aparecer no HTML
            usuario_novo = User.objects.create_user(
                username=email, 
                email=email, 
                password=senha,
                first_name=nome 
            )

            # 2. Cria o Cliente vinculado
            Cliente.objects.create(
                usuario=usuario_novo,
                nome=nome,
                cpf=cpf,
                email=email,
                telefone=telefone
            )
            
            # 3. Loga o usuário imediatamente usando o ModelBackend
            login(request, usuario_novo, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, f'Bem-vindo, {nome}!')
            return redirect('/') # Redireciona para a home

        except Exception as e:
            messages.error(request, f'Erro no cadastro: {e}')
            return render(request, 'clientes/cadastro.html')

    return render(request, 'clientes/cadastro.html')