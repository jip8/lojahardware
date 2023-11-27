from django.shortcuts import render, redirect, get_object_or_404
## from django.contrib.auth.models import User
from .models import Usuario, Produto, Cart
from django.http import HttpResponse


def home(request):
    
    usuario_id = request.session.get('usuario_id')
    nome_usuario = None

    if usuario_id:
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            nome_usuario = usuario.nome  
        except Usuario.DoesNotExist:
            pass
    produtos = Produto.objects.all()
    return render(request, 'loja/home.html', {'nome_usuario': nome_usuario, 'produtos': produtos})


def registrar(request):
    if request.method == 'GET':
        return render(request, 'loja/registrar.html')
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if Usuario.objects.filter(email=email).exists():
            mensagem = 'Este email já está em uso.'
            return render(request, 'loja/registrar.html', {'mensagem': mensagem})
        
        
        novo_usuario = Usuario.objects.create(nome=nome, email=email, senha=senha)
        novo_usuario.save()
        return redirect('login')
        

def login(request):
    if request.method == 'GET':
        return render(request, 'loja/login.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        mensagem1 = 'Email não encontrado.'
        return render(request, 'loja/login.html', {'mensagem1': mensagem1})

    if usuario.senha == senha:
        request.session['usuario_id'] = usuario.id
        return redirect('home')
    else:
        mensagem2 = 'Senha incorreta.'
        return render(request, 'loja/login.html', {'mensagem2': mensagem2})

def logout(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    return redirect('login')

def admprodutos(request):
    if request.method == 'GET':
        produtos = Produto.objects.all()
        return render(request, 'loja/admprodutos.html', {'produtos': produtos})
    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        estoque = request.POST.get('estoque')
        imagem = request.FILES.get('imagem')
        novo_prod = Produto.objects.create(nome=nome, preco=preco, estoque=estoque, imagem=imagem)
        novo_prod.save()
        return redirect('admprodutos')

def alt_prod(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'GET':
        return render(request, 'alt_prod.html', {'produto': produto})
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        estoque = request.POST.get('estoque')
        imagem = request.FILES.get('imagem')

        if nome: 
            produto.nome = nome

        if preco:  
            produto.preco = preco

        if estoque:
            produto.estoque = estoque

        if imagem:
            produto.imagem = imagem

        produto.save()
        return redirect('admprodutos')
    
def rmv_prod(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    produto.delete()
    return redirect('admprodutos')


def carrinho(request):
    usuario_id = request.session.get('usuario_id')
    nome_usuario = None
    cart = None  
    if usuario_id:
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            nome_usuario = usuario.nome  
            
            cart = Cart.objects.filter(usuario=usuario).first()
            
        except Usuario.DoesNotExist:
            pass

    return render(request, 'loja/carrinho.html', {'nome_usuario': nome_usuario, 'cart': cart})

    
def adicionar_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        cart, created = Cart.objects.get_or_create(usuario=usuario)
        cart.produtos.add(produto)
        cart.save()
        return redirect('home')
    else:
        return redirect('login')
    
def remover_item(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        cart = Cart.objects.get(usuario=usuario)
        cart.remover_item(produto)
        return redirect('carrinho')
    else:
        return redirect('login')