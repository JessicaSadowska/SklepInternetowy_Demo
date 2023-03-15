import json

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View

from Konta.models import Adres
from Koszyki.models import Koszyk, ProduktKoszyka
from Koszyki.views import _get_cart_id, _get_cart_items
from Zamówienia.models import Order, OrderProduct
from Zamówienia.forms import OrderForm


class CheckoutStep1(View):
    def load_form(self, request):
        first_name = None
        last_name = None
        email = None
        phone = None
        is_address_company = None
        company_name = None
        nip = None
        street_and_house_nr = None
        zipcode = None
        city = None
        country = None
        is_shipping_address_company = None
        company_name_shipment = None
        nip_shipment = None
        street_shipment = None
        zipcode_shipment = None
        city_shipment = None
        country_shipment = None
        order_note = None
        other_shipping_address = None
        addresses = None

        try:
            cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
            order = Order.objects.get(cart=cart)
            shipping = order.delivery_method

            if shipping in ['KurierDPD', 'Darmowa', 'KurierUE']:
                delivery_method = True

                if request.user.is_authenticated:
                    addresses = request.user.adres_set.all()

                if order.street_and_house_nr:
                    if order.is_address_company:
                        is_address_company = True
                        company_name = order.company_name
                        nip = order.nip
                    street_and_house_nr = order.street_and_house_nr
                    zipcode = order.zipcode
                    city = order.city
                    country = order.country

                if order.other_shipping_address:
                    if order.is_shipping_address_company:
                        is_shipping_address_company = True
                        company_name_shipment = order.company_name_shipment
                        nip_shipment = order.nip_shipment
                    other_shipping_address = True
                    street_shipment = order.street_shipment
                    zipcode_shipment = order.zipcode_shipment
                    city_shipment = order.city_shipment
                    country_shipment = order.country_shipment

            else:
                delivery_method = False

            if request.user.is_authenticated:
                first_name = order.user.name
                email = order.user.email

                if request.user.last_name:
                    last_name = request.user.last_name

                if request.user.phone:
                    phone = request.user.phone

            if order.last_name:
                last_name = order.last_name
                phone = order.phone
                first_name = order.first_name
                email = order.email

            if order.order_note:
                order_note = order.order_note

            initial_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'is_address_company': is_address_company,
                'company_name': company_name,
                'nip': nip,
                'street_and_house_nr': street_and_house_nr,
                'zipcode': zipcode,
                'city': city,
                'country': country,
                'other_shipping_address': other_shipping_address,
                'is_shipping_address_company': is_shipping_address_company,
                'company_name_shipment': company_name_shipment,
                'nip_shipment': nip_shipment,
                'street_shipment': street_shipment,
                'zipcode_shipment': zipcode_shipment,
                'city_shipment': city_shipment,
                'country_shipment': country_shipment,
                'order_note': order_note,

            }

            order_form = OrderForm(initial=initial_data)
            context = {
                'delivery_method': delivery_method,
                'addresses': addresses,
                'form': order_form,
            }
            return render(request, 'checkout_step1.html', context)

        except ObjectDoesNotExist:
            return redirect('Cart')

    def get(self, request):
        return self.load_form(request)

    def post(self, request):
        cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
        order = Order.objects.get(cart=cart)
        address = Adres()
        shipping_address = Adres()

        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order.first_name = order_form.cleaned_data['first_name']
            order.last_name = order_form.cleaned_data['last_name']
            order.email = order_form.cleaned_data['email']
            order.phone = order_form.cleaned_data['phone']
            order.order_note = order_form.cleaned_data['order_note']
            order.ip = request.META.get('REMOTE_ADDR')
            order.is_address_company = order_form.cleaned_data['is_address_company']
            order.other_shipping_address = order_form.cleaned_data['other_shipping_address']
            order.is_shipping_address_company = order_form.cleaned_data['is_shipping_address_company']

            order.save()

            if order.delivery_method in ['KurierDPD', 'Darmowa', 'KurierUE']:
                if order.is_address_company:
                    order.company_name = order_form.cleaned_data['company_name']
                    order.nip = order_form.cleaned_data['nip']
                order.street_and_house_nr = order_form.cleaned_data['street_and_house_nr']
                order.zipcode = order_form.cleaned_data['zipcode']
                order.city = order_form.cleaned_data['city']
                order.country = order_form.cleaned_data['country']

            order.save()

            if request.user.is_authenticated and request.POST.get('save-address', False):
                address.user = request.user
                address.street_and_house_nr = order_form.cleaned_data['street_and_house_nr']
                address.zipcode = order_form.cleaned_data['zipcode']
                address.city = order_form.cleaned_data['city']
                address.country = order_form.cleaned_data['country']
                if order.is_address_company:
                    address.company_name = order_form.cleaned_data['company_name']
                    address.nip = order_form.cleaned_data['nip']
                address.save()

            if order_form.cleaned_data['other_shipping_address']:
                if order.is_shipping_address_company:
                    order.company_name_shipment = order_form.cleaned_data['company_name_shipment']
                    order.nip_shipment = order_form.cleaned_data['nip_shipment']
                order.street_shipment = order_form.cleaned_data['street_shipment']
                order.zipcode_shipment = order_form.cleaned_data['zipcode_shipment']
                order.city_shipment = order_form.cleaned_data['city_shipment']
                order.country_shipment = order_form.cleaned_data['country_shipment']
                order.save()

                if request.user.is_authenticated and request.POST.get('save-shipping-address', False):
                    shipping_address.user = request.user
                    shipping_address.street_and_house_nr = order_form.cleaned_data['street_shipment']
                    shipping_address.zipcode = order_form.cleaned_data['zipcode_shipment']
                    shipping_address.city = order_form.cleaned_data['city_shipment']
                    shipping_address.country = order_form.cleaned_data['country_shipment']
                    if order.is_shipping_address_company:
                        address.company_name = order_form.cleaned_data['company_name']
                        address.nip = order_form.cleaned_data['nip']
                    shipping_address.save()
            else:
                order.company_name_shipment = None
                order.nip_shipment = None
                order.street_shipment = None
                order.zipcode_shipment = None
                order.city_shipment = None
                order.country_shipment = None
                order.save()

            return redirect('CheckoutStep2')

        else:
            messages.error(request, 'Wprowadź poprawny adres wysyłki')
            return self.load_form(request)


class FillAddress(View):
    def post(self, request):
        data = json.loads(request.body)
        address_id = data['selectedValue']

        address = Adres.objects.get(id=address_id)
        address_dict = {
            'company_name': address.company_name,
            'nip': address.nip,
            'street_and_house_nr': address.street_and_house_nr,
            'zipcode': address.zipcode,
            'city': address.city,
            'country': address.country,
        }
        data = json.dumps(address_dict)
        return JsonResponse(data, safe=False)


class CheckoutStep2(View):
    def get(self, request):
        try:
            cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
            order = Order.objects.get(cart=cart)
            return render(request, 'checkout_step2.html')

        except ObjectDoesNotExist:
            return redirect('Cart')


class CheckoutStep3(View):
    def get(self, request):
        try:
            cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
            order = Order.objects.get(cart=cart)

            delivery_price = 0
            if order.delivery_method == 'KurierDPD':
                delivery_price = '20,00 zł'
            elif order.delivery_method == 'KurierUE':
                delivery_price = '60,00 zł'

            cart_items = _get_cart_items(request)
            context = {
                'cart_items': cart_items,
                'order': order,
                'delivery_price': delivery_price,
            }

            return render(request, 'checkout_step3.html', context)

        except ObjectDoesNotExist:
            return redirect('Cart')

    def post(self, request):
        try:
            cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
            if cart.id_koszyka == request.session.session_key:
                order = Order.objects.get(cart=cart)

                order.status = 'Potwierdzone'
                order.save()

                cart_items = _get_cart_items(request)

                for item in cart_items:
                    order_product = OrderProduct()
                    order_product.order_id = order.id
                    if request.user.is_authenticated:
                        order_product.user_id = request.user.id
                    order_product.product_id = item.produkt_id
                    order_product.quantity = item.ilosc
                    order_product.product_price = item.wartosc
                    order_product.is_ordered = True
                    order_product.save()

                for item in cart_items:
                    ProduktKoszyka.objects.get(id=item.id).delete()

                mail_subject = "Potwierdzenie zamówienia"
                message = render_to_string('order_confirmation_email.html', {
                    'first_name': order.first_name,
                    'last_name': order.last_name,
                    'order': order,
                })
                from_email = 'Piernikowa Kusica'
                send_email_to = order.email
                send_email = EmailMessage(mail_subject, message, from_email=from_email, to=[send_email_to])
                send_email.send()

                request.session.flush()

            else:
                return redirect('Cart')

        except ObjectDoesNotExist:
            return redirect('Cart')

        context = {
            'name': order.first_name
        }
        return render(request, 'order_confirmation.html', context)
