from django.contrib import admin
from PiernikowaKusica.models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('nazwa',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'cena',)
    search_fields = ('nazwa',)
    prepopulated_fields = {'url': ('nazwa', 'cena')}


admin.site.register(Kategoria, CategoryAdmin)
admin.site.register(Produkt, ProductAdmin)
admin.site.register(PolecaneProdukty)
