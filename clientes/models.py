from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    # Relacionamento 1:1 com o usuário do sistema
    # null=True e blank=True permitem que clientes antigos continuem existindo sem usuário
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Usuário Relacionado")
    
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome