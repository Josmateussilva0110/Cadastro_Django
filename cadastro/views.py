from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from cadastro.forms import Register_User


def index(request):
    return render(request, 'cadastro/pages/index.html')

def register_user(request):
    context = dict()
    if request.method == 'POST':
        form = Register_User(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect('cadastro:register_user')
    else:
        form = Register_User()
    context['form'] = form
    context['page_title'] = 'Cadastro'
    return render(request, 'cadastro/pages/cadastrar.html', context)
