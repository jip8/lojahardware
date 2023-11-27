from django.db import models
from django.forms import ModelForm

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return f"Usuário: {self.nome}, Email: {self.email}"

class Cart(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    produtos = models.ManyToManyField('Produto', related_name='carrinhos', blank=True)

    def calcTot(self):
        total = sum(produto.preco for produto in self.produtos.all())
        return total

    def remover_item(self, produto):
        if produto in self.produtos.all():
            self.produtos.remove(produto)

    def __str__(self):
        return f"Carrinho do usuário: {self.usuario}"

    class Meta:
        verbose_name_plural = "Carrinhos"

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f}, Estoque: {self.estoque} (ID: {self.id})"

class ComponenteHardware(Produto):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.marca} {self.modelo} - {super().__str__()}"

class Periferico(Produto):
    alimentacao = models.CharField(max_length=100)
    conexao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.conexao} - {self.alimentacao}) - {super().__str__()}"
