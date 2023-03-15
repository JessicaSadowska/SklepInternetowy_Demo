from .models import Koszyk, ProduktKoszyka
from .views import _get_cart_id


def item_counter(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Koszyk.objects.filter(id_koszyka=_get_cart_id(request))
            if request.user.is_authenticated:
                cart_items = ProduktKoszyka.objects.all().filter(uzytkownik=request.user)
            else:
                cart_items = ProduktKoszyka.objects.all().filter(koszyk=cart[:1])
            no_cart_items = cart_items.count()
        except Koszyk.DoesNotExist:
            no_cart_items = 0
        return dict(no_cart_items=no_cart_items)


def get_cart_items(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Koszyk.objects.filter(id_koszyka=_get_cart_id(request))
            if request.user.is_authenticated:
                global_cart_items = ProduktKoszyka.objects.all().filter(uzytkownik=request.user)
            else:
                global_cart_items = ProduktKoszyka.objects.all().filter(koszyk=cart[:1])
        except Koszyk.DoesNotExist:
            global_cart_items = None
        return dict(global_cart_items=global_cart_items)


def get_total(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                cart_items = ProduktKoszyka.objects.all().filter(uzytkownik=request.user)
            else:
                cart = Koszyk.objects.filter(id_koszyka=_get_cart_id(request))
                cart_items = ProduktKoszyka.objects.all().filter(koszyk=cart[:1])
            global_total = 0
            for item in cart_items:
                global_total += item.wartosc
            amount_to_free_delivery = 300 - global_total
        except Koszyk.DoesNotExist:
            global_total = None
            amount_to_free_delivery = None
        return dict(global_total=global_total, amount_to_free_delivery=amount_to_free_delivery)
