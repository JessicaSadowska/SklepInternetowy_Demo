import datetime
import json

from django.contrib import auth, messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View

from Konta.models import Uzytkownik, Adres
from Koszyki.models import Koszyk, ProduktKoszyka
from PiernikowaKusica.models import Produkt
from Zamówienia.models import Order


def _get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def _get_cart_items(request):
    if request.user.is_authenticated:
        cart_items = ProduktKoszyka.objects.all().filter(uzytkownik=request.user)
    else:
        cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
        cart_items = ProduktKoszyka.objects.filter(koszyk=cart, aktywny=True)
    return cart_items


class UpdateCart(View):
    def post(self, request):
        data = json.loads(request.body)
        product_id = data['productId']
        action = data['action']

        product = Produkt.objects.get(id=product_id)

        if action == 'add':
            # user authenticated
            if request.user.is_authenticated:
                does_cart_item_exist = ProduktKoszyka.objects.filter(produkt=product, uzytkownik=request.user).exists()
                if does_cart_item_exist:
                    cart_item = ProduktKoszyka.objects.get(produkt=product, uzytkownik=request.user)
                    if data['quantity']:
                        cart_item.ilosc += int(data['quantity'])
                        cart_item.wartosc += product.cena * int(data['quantity'])
                    else:
                        cart_item.ilosc += 1
                        cart_item.wartosc += product.cena
                    cart_item.save()
                else:
                    if data['quantity']:
                        ilosc = int(data['quantity'])
                        wartosc = product.cena * int(data['quantity'])
                    else:
                        ilosc = 1
                        wartosc = product.cena

                    cart_item = ProduktKoszyka.objects.create(
                        produkt=product,
                        uzytkownik=request.user,
                        ilosc=ilosc,
                        wartosc=wartosc,
                    )
                    cart_item.save()

            # user not authenticated
            else:
                try:
                    cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
                except Koszyk.DoesNotExist:
                    cart = Koszyk.objects.create(
                        id_koszyka=_get_cart_id(request)
                    )
                    cart.save()

                does_cart_item_exist = ProduktKoszyka.objects.filter(produkt=product, koszyk=cart).exists()
                if does_cart_item_exist:
                    cart_item = ProduktKoszyka.objects.get(produkt=product, koszyk=cart)
                    if data['quantity']:
                        cart_item.ilosc += int(data['quantity'])
                        cart_item.wartosc += product.cena * int(data['quantity'])
                    else:
                        cart_item.ilosc += 1
                        cart_item.wartosc += product.cena
                    cart_item.save()
                else:
                    if data['quantity']:
                        ilosc = int(data['quantity'])
                        wartosc = product.cena * int(data['quantity'])
                    else:
                        ilosc = 1
                        wartosc = product.cena

                    cart_item = ProduktKoszyka.objects.create(
                        produkt=product,
                        koszyk=cart,
                        ilosc=ilosc,
                        wartosc=wartosc,
                    )
                    cart_item.save()

        elif action == "remove":
            if request.user.is_authenticated:
                cart_item = ProduktKoszyka.objects.get(produkt=product, uzytkownik=request.user)
            else:
                cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
                cart_item = ProduktKoszyka.objects.get(produkt=product, koszyk=cart)

            if cart_item.ilosc > 1:
                cart_item.ilosc -= 1
                cart_item.wartosc -= cart_item.produkt.cena
                cart_item.save()
            else:
                cart_item.delete()

        return JsonResponse('item added successfully', safe=False)


class AddToCart(View):
    def get(self, request, product_id):
        product = Produkt.objects.get(id=product_id)

        # user authenticated
        if request.user.is_authenticated:
            does_cart_item_exist = ProduktKoszyka.objects.filter(produkt=product, uzytkownik=request.user).exists()
            if does_cart_item_exist:
                cart_item = ProduktKoszyka.objects.get(produkt=product, uzytkownik=request.user)
                cart_item.ilosc += 1
                cart_item.wartosc += product.cena
                cart_item.save()
            else:
                cart_item = ProduktKoszyka.objects.create(
                    produkt=product,
                    uzytkownik=request.user,
                    ilosc=1,
                    wartosc=product.cena,
                )
                cart_item.save()
            return redirect('Cart')

        # user not authenticated
        else:
            try:
                cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
            except Koszyk.DoesNotExist:
                cart = Koszyk.objects.create(
                    id_koszyka=_get_cart_id(request)
                )
                cart.save()

            does_cart_item_exist = ProduktKoszyka.objects.filter(produkt=product, koszyk=cart).exists()
            if does_cart_item_exist:
                cart_item = ProduktKoszyka.objects.get(produkt=product, koszyk=cart)
                cart_item.ilosc += 1
                cart_item.wartosc += product.cena
                cart_item.save()
            else:
                cart_item = ProduktKoszyka.objects.create(
                    produkt=product,
                    koszyk=cart,
                    ilosc=1,
                    wartosc=product.cena,
                )
                cart_item.save()
            return redirect('Cart')


class RemoveFromCart(View):
    def get(self, request, product_id):
        product = get_object_or_404(Produkt, id=product_id)

        if request.user.is_authenticated:
            cart_item = ProduktKoszyka.objects.get(produkt=product, uzytkownik=request.user)
        else:
            cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
            cart_item = ProduktKoszyka.objects.get(produkt=product, koszyk=cart)

        if cart_item.ilosc > 1:
            cart_item.ilosc -= 1
            cart_item.wartosc -= cart_item.produkt.cena
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('Cart')


class RemoveCartItem(View):
    def get(self, request, product_id):
        product = get_object_or_404(Produkt, id=product_id)

        if request.user.is_authenticated:
            cart_item = ProduktKoszyka.objects.get(produkt=product, uzytkownik=request.user)
        else:
            cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
            cart_item = ProduktKoszyka.objects.get(produkt=product, koszyk=cart)

        cart_item.delete()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class Cart(View):
    def get(self, request, cart_items=None):
        try:
            if request.user.is_authenticated:
                cart_items = ProduktKoszyka.objects.all().filter(uzytkownik=request.user)
            else:
                cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
                cart_items = ProduktKoszyka.objects.filter(koszyk=cart, aktywny=True)
        except ObjectDoesNotExist:
            pass

        context = {
            'cart_items': cart_items,
        }
        return render(request, 'cart.html', context)

    def post(self, request):
        try:
            shipping = request.POST['shipping']

            try:
                cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
            except Koszyk.DoesNotExist:
                cart = Koszyk.objects.create(
                    id_koszyka=_get_cart_id(request)
                )
                cart.save()

            try:
                order = Order.objects.get(cart=cart)
            except ObjectDoesNotExist:
                order = Order()
                order.cart = cart

            order.delivery_method = shipping

            if request.user.is_authenticated:
                order.user = request.user

            cart_items = _get_cart_items(request)

            order_total = 0
            for item in cart_items:
                order_total += item.wartosc
            if shipping == 'KurierDPD':
                order_total += 20
            elif shipping == 'KurierUE':
                order_total += 60

            order.order_total = order_total
            order.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%y%m%d")
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()
            if request.user.is_authenticated:
                return redirect('CheckoutStep1')
            else:
                return redirect('GoToCheckout')

        except MultiValueDictKeyError:
            messages.error(request, 'Wybierz sposób dostawy')
            return redirect('Cart')


class GoToCheckout(View):
    def get(self, request):
        return render(request, 'go_to_checkout.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user:
            users_products = []
            for item in user.produktkoszyka_set.all():
                users_products.append(item.produkt)
            try:
                cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
                does_cart_item_exist = ProduktKoszyka.objects.filter(koszyk=cart).exists()
                if does_cart_item_exist:
                    cart_items = ProduktKoszyka.objects.filter(koszyk=cart)
                    for item in cart_items:
                        if item.produkt in users_products:
                            existing_users_item = ProduktKoszyka.objects.get(produkt=item.produkt, uzytkownik=user)
                            existing_users_item.ilosc += 1
                            existing_users_item.save()
                        else:
                            item.uzytkownik = user
                        item.save()
            except ObjectDoesNotExist:
                pass

            auth.login(request, user)
            if users_products:
                messages.success(request, 'Zalogowano! W Twoim koszyku znajdują się jeszcze inne produkty.')
                return redirect('Cart')
            else:
                messages.success(request, 'Zalogowano!')
                return redirect('CheckoutStep1')
        else:
            if Uzytkownik.objects.filter(email=email).exists():
                u = Uzytkownik.objects.get(email__exact=email)
                if not u.is_active:
                    messages.error(request, 'Konto nie zostało aktywowane. Sprawdź pocztę i kliknij w link aktywacyjny.')
                else:
                    messages.error(request, 'Niepoprawne dane logowania.')
            else:
                messages.error(request, 'Niepoprawne dane logowania.')
            return redirect('Checkout')
