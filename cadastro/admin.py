from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = 'id', 'username', 'first_name', 'last_name', 'email',
    list_display_links = 'id', 'username', 'first_name',
    search_fields = 'id', 'username', 'first_name', 'last_name', 'email',
    list_per_page = 10
    ordering = '-id',
