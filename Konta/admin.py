from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Konta.models import *


class AccountAdmin(UserAdmin):
    ordering = ('-date_joined',)
    list_display = ('email', 'name', 'last_login', 'date_joined', 'is_active')
    search_fields = ('email',)
    readonly_fields = ('email', 'newsletter', 'last_login', 'date_joined', 'is_active', 'is_admin', 'is_superuser', 'is_staff')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    exclude = ('username',)


admin.site.register(Uzytkownik, AccountAdmin)
admin.site.register(Adres)
