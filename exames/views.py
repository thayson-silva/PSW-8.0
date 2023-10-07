from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TiposExames, SolicitacaoExame, PedidosExames
from django.http import HttpResponse
from datetime import datetime
from django.contrib.messages import constants
from django.contrib import messages

@login_required #se não estiver com usuario na sessão ele da um 404
def solicitar_exames(request):
    context = {
        'tipos_exames' : TiposExames.objects.all(),
    }

    if request.method == 'GET':
        return render(request, 'solicitar_exames.html', context=context)
    elif request.method == 'POST':
        exames_id = request.POST.getlist('exames')
        exames_solicitados = TiposExames.objects.filter(pk__in = exames_id)

        total = 0
        for i in exames_solicitados:
            if i.disponivel:
                total += i.preco        

        context['exames_solicitados'] = exames_solicitados
        context['total'] = total
        return render(request, 'solicitar_exames.html', context=context)

@login_required        
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')  
    solicitacao_exames  = TiposExames.objects.filter(pk__in = exames_id)
    
    pedido_exame = PedidosExames(
        usuario = request.user,
        data = datetime.now()
    )
    pedido_exame.save()
    
    for exame in solicitacao_exames :
        exame_solicitado = SolicitacaoExame(
            usuario = request.user,
            exame = exame
        )
        exame_solicitado.save()
        pedido_exame.exames.add(exame_solicitado)

    messages.add_message(request, constants.SUCCESS, 'Pedido de exame concluído com sucesso')
    return redirect('/exames/gerenciar_pedidos/')

@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})

@login_required
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id = pedido_id)

    if request.user != pedido.usuario:
        messages.add_message(request, constants.ERROR, 'Não é possivel cancelar um pedido que não é seu!')
        return redirect('/exames/gerenciar_pedidos/')
        
    pedido.agendado = False
    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido cancelado com sucesso!')
    return redirect('/exames/gerenciar_pedidos/')

@login_required
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario = request.user)
    return render(request, 'gerenciar_exames.html', {'exames' : exames})

@login_required
def permitir_abrir_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id = exame_id)
    if not exame.requer_senha:
        return redirect(exame.resultado.url)
    
    return redirect(f'/exames/solicitar_senha_exame/{exame.id}')

@login_required
def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(pk = exame_id)

    if request.method == 'GET':
        return render(request, 'solicitar_senha_exame.html', {'exame': exame})
    elif request.method == 'POST':
        senha_informada = request.POST.get('senha')

        if senha_informada == exame.senha:
            return redirect(exame.resultado.url)
        
        messages.add_message(request, constants.ERROR, 'Senha incorreta!')
        return redirect(f'/exames/solicitar_senha_exame/{exame.id}')

#para testar o código
# print("")
# print(pedido_id)
# print("")
