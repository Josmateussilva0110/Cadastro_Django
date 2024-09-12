from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cadastro.forms import Register_User, Login_user, Update_User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required


PER_PAGE = 8

def index(request):
    context = dict()
    users = User.objects.all().filter(is_staff=False)
    context['number_people'] = len(users)
    return render(request, 'cadastro/pages/index.html', context)


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
    


@login_required(login_url='cadastro:login_user')
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('cadastro:index')
    else:
        return render(request, 'cadastro/pages/logout.html')


@login_required(login_url='cadastro:login_user')
def list_users(request):
    context = dict()
    users = User.objects.filter(is_staff=False).order_by('-id')
    if not users:
        raise Http404()
    paginator = Paginator(users, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['page_title'] = 'Lista de Usuários' 
    return render(request, 'cadastro/pages/list_users.html', context)


@login_required(login_url='cadastro:login_user')
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


@login_required(login_url='cadastro:login_user')
def view_user(request, id):
    context = dict()
    current_user = get_object_or_404(User, is_staff=False, id=id)
    context['page_title'] = current_user
    context['current_user'] = current_user
    return render(request, 'cadastro/pages/view_user.html', context)


@login_required(login_url='cadastro:login_user')
def update_user(request, id):
    context = dict()
    current_user = get_object_or_404(User, is_staff=False, id=id)
    
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


@login_required(login_url='cadastro:login_user')
def delete_user(request, id):
    context = dict()
    current_user = get_object_or_404(User, is_staff=False, id=id)
    if request.method == 'POST':
        current_user.delete()
        messages.success(request, 'Usuário deletado com sucesso.')
        return redirect('cadastro:index')

    context['page_title'] = 'Delete User'
    context['current_user'] = current_user
    return render(request, 'cadastro/pages/delete_user.html', context)
