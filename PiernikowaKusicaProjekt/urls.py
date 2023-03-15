from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from PiernikowaKusica.views import *
from Koszyki.views import *
from Konta.views import *
from Zamówienia.views import *
from PiernikowaKusicaProjekt import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='HomePage'),
    path('sklep-online/', OnlineShop.as_view(), name='OnlineShop'),
    path('sklep-online/<slug:category_url>/', OnlineShopByCategory.as_view(), name='ProductsByCategory'),
    path('sklep-online/<slug:category_url>/<slug:product_url>/', OnlineShopProductDetail.as_view(), name='OnlineShopProductDetail'),
    path('zamowienia/', Orders.as_view(), name='Orders'),
    path('o-nas/', AboutUs.as_view(), name='AboutUs'),
    path('kontakt/', Contact.as_view(), name='Contact'),
    path('informacje/', Information.as_view(), name='Information'),
    path('koszyk/', Cart.as_view(), name='Cart'),
    path('edytuj-koszyk/', UpdateCart.as_view(), name='UpdateCart'),
    path('dodaj-do-koszyka/<int:product_id>/', AddToCart.as_view(), name='AddToCart'),
    path('usun-z-koszyka/<int:product_id>/', RemoveFromCart.as_view(), name='RemoveFromCart'),
    path('usun-produkt/<int:product_id>/', RemoveCartItem.as_view(), name='RemoveCartItem'),
    path('szukaj/', Search.as_view(), name='Search'),
    path('rejestracja/', Register.as_view(), name='Register'),
    path('logowanie/', Login.as_view(), name='Login'),
    path('aktywacja/<uidb64>/<token>/', Activate.as_view(), name='Activate'),
    path('wyloguj/', Logout.as_view(), name='Logout'),
    path('edycja-profilu/', Dashboard.as_view(), name='Dashboard'),
    path('edycja-profilu/lista-adresow/', AddressList.as_view(), name='AddressList'),
    path('edycja-profilu/lista-adresow/<int:address_id>/', DeleteAddress.as_view(), name='DeleteAddress'),
    path('zmiana-hasla/', ChangePassword.as_view(), name='ChangePassword'),
    path('moje-zamowienia/', ClientsOrders.as_view(), name='ClientsOrders'),
    path('moje-zamowienia/<int:order_number>/', ClientsOrderDetail.as_view(), name='ClientsOrderDetail'),
    path('logowanie/odzyskiwanie-hasla/', ForgotPassword.as_view(), name='ForgotPassword'),
    path('logowanie/odzyskiwanie-hasla/<uidb64>/<token>/', ResetPasswordValidation.as_view(), name='ResetPasswordValidation'),
    path('logowanie/odzyskiwanie-hasla/nowe-haslo/', ResetPassword.as_view(), name='ResetPassword'),
    path('kasa/', GoToCheckout.as_view(), name='GoToCheckout'),
    path('kasa/dane/', CheckoutStep1.as_view(), name='CheckoutStep1'),
    path('kasa/metoda-platnosci/', CheckoutStep2.as_view(), name='CheckoutStep2'),
    path('kasa/podsumowanie/', CheckoutStep3.as_view(), name='CheckoutStep3'),
    path('wypelnij-adres/', FillAddress.as_view(), name='FillAddress'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
