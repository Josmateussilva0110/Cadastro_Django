from django.urls import path
from cadastro.views import *

app_name = 'cadastro'

urlpatterns = [
    path('', index, name='index'),
    path('register_user/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('list_users/', list_users, name='list_users'),
]