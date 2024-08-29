from django.urls import path
from cadastro.views import *

app_name = 'cadastro'

urlpatterns = [
    path('', index, name='index'),
    path('register_user/', register_user, name='register_user'),
]