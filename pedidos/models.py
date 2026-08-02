from django.db import models
from django.contrib.auth.models import User
from produtos.models import Produto
from clientes.models import Cliente

class Pedido(models.Model):
    # Vincula o pedido ao usuário do sistema para controle de login e histórico
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    
    # Mantém o vínculo com Cliente para dados adicionais de cadastro
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    
    # Relação ManyToMany para permitir múltiplos itens no mesmo pedido
    produtos = models.ManyToManyField(Produto, verbose_name="Produtos")
    
    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pedido")
    pago = models.BooleanField(default=False, verbose_name="Pedido Pago")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        # Exibe o ID e o nome do usuário no painel administrativo
        return f"Pedido {self.id} - {self.usuario.username}"