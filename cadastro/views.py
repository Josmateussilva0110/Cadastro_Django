from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from cadastro.forms import Register_User, Login_user, Update_User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required


PER_PAGE = 8


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
    paginator = Paginator(users, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['page_title'] = 'Lista de Usuários' 
    return render(request, 'cadastro/pages/list_users.html', context)


def search(request):
    context = dict()
    search_value = request.GET.get('search', '').strip()

    users = User.objects.filter(Q(username__icontains=search_value) | Q(first_name__icontains=search_value) | Q(email__icontains=search_value) | Q(last_name__icontains=search_value)).filter(is_staff=False)

    paginator = Paginator(users, PER_PAGE)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['page_title'] = f'{search_value[:20]}'
    context['search_value'] = search_value
    context['page_obj'] = page_obj  

    return render(request, 'cadastro/pages/list_users.html', context)

@login_required
def view_user(request, id):
    context = dict()
    current_user = User.objects.filter(is_staff=False).filter(id=id).first()
    if current_user is None:
        raise Http404
    context['page_title'] = current_user
    context['current_user'] = current_user
    return render(request, 'cadastro/pages/view_user.html', context)


@login_required
def update_user(request, id):
    context = dict()
    current_user = User.objects.filter(is_staff=False).filter(id=id).first()
    
    if not current_user:
        messages.error(request, 'Usuário não encontrado.')
        return redirect('cadastro:index')
    
    if request.method == 'POST':
        form = Update_User(data=request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso.')
            return redirect('cadastro:update_user', id=current_user.id)
        else:
            context['form'] = form
    else:
        form = Update_User(instance=current_user)
        context['form'] = form
    
    context['current_user'] = current_user
    context['page_title'] = 'Update User'
    return render(request, 'cadastro/pages/update_user.html', context)


@login_required
def delete_user(request, id):
    context = dict()
    current_user = User.objects.filter(is_staff=False).filter(id=id).first()
    confirmation = request.POST.get('confirmation', 'no')
    if not current_user:
        messages.error(request, 'Usuário não encontrado.')
        return redirect('cadastro:index')
    if request.method == 'POST':
        current_user.delete()
        messages.success(request, 'Usuário deletado com sucesso.')
        return redirect('cadastro:index')

    context['page_title'] = 'Delete User'
    context['current_user'] = current_user
    context['confirmation'] = confirmation
    return render(request, 'cadastro/pages/delete_user.html', context)
