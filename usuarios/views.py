from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'Senha menor que 6 caracteres')
            return redirect('/usuarios/cadastro')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/usuarios/cadastro')
        
        if User.objects.get(username = username):
            messages.add_message(request, constants.ERROR, 'Username já existente')
            return redirect('/usuarios/cadastro')
              
        try:
            user = User.objects.create_user(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                username=username,
                email = email,
                password = senha,
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
        # except IntegrityError:
        #     messages.add_message(request, constants.ERROR, 'Usuário ja existente na base de dados!')
        #     return redirect('/usuarios/cadastro')
        except:
            messages.add_message(request, constants.ERROR, 'erro interno, contact um administrador!')
            return redirect('/usuarios/cadastro')

        return redirect('/usuarios/cadastro')
    
def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        #authenticate() verifica se existe o usuario e senha na bd
        user = authenticate(username=username, password=senha)
        if user:
            print()
            print(request)
            print(request.user) #AnonymousUser
            print()

            #loga com usuario e joga ele na sessão
            login(request, user)

            print()
            print(request)
            print(request.user) #Nome do usuario logado
            print()
            return HttpResponse(f"BEM VINDO {user}")
        else:
            messages.add_message(request, constants.ERROR, 'Usuário e senha inválidos!')
            return redirect('/usuarios/login')
        
        