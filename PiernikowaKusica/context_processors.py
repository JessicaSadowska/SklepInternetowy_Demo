from django.core.exceptions import ObjectDoesNotExist

from .models import Kategoria, PolecaneProdukty


def fetch_all_categories(request):
    all_categories = Kategoria.objects.all()
    return dict(all_categories=all_categories)


def fetch_recommended_products(request):
    try:
        recommended = PolecaneProdukty.objects.get(nazwa='Polecane produkty')
        recommended_products = recommended.produkty.all()
    except ObjectDoesNotExist:
        recommended_products = None
    return dict(recommended_products=recommended_products)
