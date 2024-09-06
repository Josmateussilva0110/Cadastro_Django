from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from cadastro.forms import Register_User, Login_user
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator



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


def login_user(request):
    context = dict()
    if request.method == 'POST':
        form = Login_user(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso.')
                context['login_success'] = True
            else:
                messages.error(request, 'Login inválido.')
    else:
        form = Login_user()
    context['form'] = form
    context['page_title'] = 'Login'
    return render(request, 'cadastro/pages/login.html', context)


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('cadastro:index')
    else:
        return render(request, 'cadastro/pages/logout.html')


def list_users(request):
    context = dict()
    users = User.objects.filter(is_staff=False).order_by('-id')
    paginator = Paginator(users, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['page_title'] = 'Lista de Usuários' 
    return render(request, 'cadastro/pages/list_users.html', context)
