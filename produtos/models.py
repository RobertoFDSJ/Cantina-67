from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(verbose_name="Descrição", blank=True)
    preco = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Preço")
    imagem = models.ImageField(upload_to='salgados/', verbose_name="Imagem do Salgado")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome