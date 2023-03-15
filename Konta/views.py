from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from Konta.forms import RegistrationForm, PersonalDetailsForm, AddressForm
from Konta.models import Uzytkownik, Adres
from Koszyki.models import Koszyk, ProduktKoszyka
from Koszyki.views import _get_cart_id
from Zamówienia.models import Order


class Register(View):
    def get(self, request):
        form = RegistrationForm
        context = {
            'form': form,
        }
        return render(request, 'register.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            newsletter = form.cleaned_data['newsletter']

            user = Uzytkownik.objects.create_user(email, name, newsletter, password)
            user.save()

            try:
                cart = Koszyk.objects.get(id_koszyka=_get_cart_id(request))
                does_cart_item_exist = ProduktKoszyka.objects.filter(koszyk=cart).exists()
                if does_cart_item_exist:
                    cart_items = ProduktKoszyka.objects.filter(koszyk=cart)
                    for item in cart_items:
                        item.uzytkownik = user
                        item.save()
            except:
                pass

            current_site = get_current_site(request)
            mail_subject = "Rejestracja Twojego konta"
            message = render_to_string('verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            from_email = 'Piernikowa Kusica'
            send_email_to = email
            send_email = EmailMessage(mail_subject, message, from_email=from_email, to=[send_email_to])
            send_email.send()

            messages.success(request, 'Aby potwierdzić rejestrację, sprawdź pocztę i kliknij w link aktywujący konto.')
            return redirect('Register')

        context = {
            'form': form,
        }
        messages.error(request, 'Nie udało się zarejestrować użytkownika.')
        return render(request, 'register.html', context)


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

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
            messages.success(request, 'Zalogowano!')
            return redirect('HomePage')
        else:
            if Uzytkownik.objects.filter(email=email).exists():
                u = Uzytkownik.objects.get(email__exact=email)
                if not u.is_active:
                    messages.error(request, 'Konto nie zostało aktywowane. Sprawdź pocztę i kliknij w link aktywacyjny.')
                else:
                    messages.error(request, 'Niepoprawne dane logowania.')
            else:
                messages.error(request, 'Niepoprawne dane logowania.')
            return redirect('Login')


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Uzytkownik._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Uzytkownik.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            auth.login(request, user)
            messages.success(request, 'Rejestracja przebiegła pomyślnie. Twoje konto zostało aktywowane!')
            return redirect('HomePage')
        else:
            messages.error(request, 'Link aktywacyjny stracił swoją ważność. Spróbuj ponownie.')
            return redirect('Register')


@method_decorator(login_required, name='dispatch')
class Logout(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, 'Wylogowano.')
        return redirect('Login')


@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    def get(self, request):
        initial_data = {
            'name': request.user.name,
            'last_name': request.user.last_name,
            'phone': request.user.phone,

        }
        form = PersonalDetailsForm(initial=initial_data)
        address_form = AddressForm

        context = {
            'form': form,
            'address_form': address_form
        }
        return render(request, 'dashboard.html', context)

    def post(self, request):
        form = PersonalDetailsForm(request.POST)
        user = request.user

        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']

            user.name = name
            user.last_name = last_name
            user.phone = phone
            user.save()
            messages.success(request, 'Pomyślnie zaktualizowano Twoje dane.')
            return redirect('Dashboard')

        messages.error(request, 'Nie udało się zaktualizować danych.')
        return redirect('Dashboard')


@method_decorator(login_required, name='dispatch')
class AddressList(View):
    def get(self, request):
        addresses = request.user.adres_set.all()
        return render(request, 'address_list.html', context={'addresses': addresses})

    def post(self, request):
        form = AddressForm(request.POST)
        user = request.user

        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            nip = form.cleaned_data['nip']
            street_and_house_nr = form.cleaned_data['street_and_house_nr']
            zipcode = form.cleaned_data['zipcode']
            city = form.cleaned_data['city']

            country = request.POST['country']

            address = Adres.objects.create(user=user, company_name=company_name, nip=nip,
                                           street_and_house_nr=street_and_house_nr, zipcode=zipcode,
                                           city=city, country=country)
            address.save()

            messages.success(request, 'Zapisano adres.')
            return redirect('AddressList')

        messages.error(request, 'Nie udało się zapisać adresu.')
        return redirect('Dashboard')


@method_decorator(login_required, name='dispatch')
class DeleteAddress(View):
    def get(self, request, address_id):
        address = request.user.adres_set.filter(id=address_id)
        address.delete()
        messages.success(request, "Adres został usunięty.")
        return redirect('AddressList')


@method_decorator(login_required, name='dispatch')
class ChangePassword(View):
    def get(self, request):
        return render(request, 'change_password.html')

    def post(self, request):
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        user = Uzytkownik.objects.get(email=request.user.email)

        if new_password == confirm_new_password:
            if len(new_password) >= 8:
                success = user.check_password(current_password)
                if success:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Hasło zostało zmienione.")
                    return redirect('Dashboard')
                else:
                    messages.error(request, "Niepoprawne hasło.")
                    return redirect('ChangePassword')
            else:
                messages.error(request, "Hasło jest za krótkie.")
                return redirect('ChangePassword')
        else:
            messages.error(request, "Wprowadzone hasła są różne.")
            return redirect('ChangePassword')


@method_decorator(login_required, name='dispatch')
class ClientsOrders(View):
    def get(self, request):
        orders = []
        for order in request.user.order_set.all():
            orders.append(order)
        if orders:
            orders.sort(key=lambda r: r.created_at, reverse=True)

        context = {
            'orders': orders,
        }
        return render(request, 'clients_orders.html', context)


@method_decorator(login_required, name='dispatch')
class ClientsOrderDetail(View):
    def get(self, request, order_number):
        try:
            order = Order.objects.get(order_number=order_number)
            order_products = order.orderproduct_set.all()
            delivery_price = 0
            price = order.order_total
            if order.delivery_method == 'KurierDPD':
                delivery_price = '20,00 zł'
                price = price - 20
            elif order.delivery_method == 'KurierUE':
                delivery_price = '60,00 zł'
                price = price - 60

        except ObjectDoesNotExist:
            return redirect('ClientsOrders')

        context = {
            'order': order,
            'order_products': order_products,
            'delivery_price': delivery_price,
            'price': price,
        }
        return render(request, 'clients_order_detail.html', context)


class ForgotPassword(View):
    def get(self, request):
        return render(request, 'forgot_password.html')

    def post(self, request):
        email = request.POST['email']

        if Uzytkownik.objects.filter(email=email).exists():
            user = Uzytkownik.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = "Zmiana hasła"
            message = render_to_string('forgot_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            from_email = 'Piernikowa Kusica'
            send_email_to = email
            send_email = EmailMessage(mail_subject, message, from_email=from_email, to=[send_email_to])
            send_email.send()

            messages.success(request, 'Link do zmiany hasła został wysłany na podany adres email.')
            return redirect('Login')

        else:
            messages.error(request, 'Nie istnieje konto z podanym adresem email')
            return redirect('Login')


class ResetPasswordValidation(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Uzytkownik._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Uzytkownik.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, 'Zresetuj swoje hasło')
        else:
            messages.error(request, 'Link aktywacyjny stracił swoją ważność. Spróbuj ponownie.')

        return redirect('ResetPassword')


class ResetPassword(View):
    def get(self, request):
        return render(request, 'reset_password.html')

    def post(self, request):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Uzytkownik.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Hasło zostało zmienione.')
            return redirect('Login')
        else:
            messages.error(request, 'Wprowadzone hasła są różne.')
            return redirect('ResetPassword')


