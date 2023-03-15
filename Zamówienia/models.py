from django.core.exceptions import ValidationError
from django.db import models

from Konta.models import Uzytkownik, Adres
from Koszyki.models import Koszyk
from PiernikowaKusica.models import Produkt


class Order(models.Model):
    STATUS = (
        ('Nowe', 'Nowe'),
        ('Potwierdzone', 'Potwierdzone'),
        ('Zrealizowane', 'Zrealizowane'),
        ('Skasowane', 'Skasowane'),
    )
    order_number = models.CharField(max_length=20, verbose_name='Numer zamówienia')
    cart = models.ForeignKey(Koszyk, on_delete=models.CASCADE, verbose_name='ID koszyka')
    user = models.ForeignKey(Uzytkownik, on_delete=models.SET_NULL, null=True, verbose_name='Użytkownik')
    first_name = models.CharField(max_length=50, verbose_name='Imię', blank=True)
    last_name = models.CharField(max_length=50, verbose_name='Nazwisko', blank=True)
    phone = models.CharField(max_length=15, verbose_name='Telefon', blank=True)
    email = models.EmailField(max_length=50, verbose_name='Email', blank=True)
    delivery_method = models.CharField(max_length=20, verbose_name='Sposób dostawy')
    is_address_company = models.BooleanField(default=False, verbose_name='Firma')
    company_name = models.CharField(max_length=100, verbose_name='Nazwa firmy', blank=True, null=True)
    nip = models.CharField(max_length=15, verbose_name='NIP', blank=True, null=True)
    street_and_house_nr = models.CharField(max_length=50, verbose_name='Ulica i nr domu', blank=True)
    zipcode = models.CharField(max_length=15, verbose_name='Kod pocztowy', blank=True)
    city = models.CharField(max_length=50, verbose_name='Miasto', blank=True)
    country = models.CharField(max_length=50, verbose_name='Kraj', blank=True)
    other_shipping_address = models.BooleanField(default=False, verbose_name='Inny adres wysyłki')
    is_shipping_address_company = models.BooleanField(default=False, verbose_name='Firma WYSYŁKA')
    company_name_shipment = models.CharField(max_length=100, verbose_name='Nazwa firmy WYSYŁKA', blank=True, null=True)
    nip_shipment = models.CharField(max_length=15, verbose_name='NIP WYSYŁKA', blank=True, null=True)
    street_shipment = models.CharField(max_length=50, verbose_name='Ulica i nr domu WYSYŁKA', blank=True, null=True)
    zipcode_shipment = models.CharField(max_length=15, verbose_name='Kod pocztowy WYSYŁKA', blank=True, null=True)
    city_shipment = models.CharField(max_length=50, verbose_name='Miasto WYSYŁKA', blank=True, null=True)
    country_shipment = models.CharField(max_length=50, verbose_name='Kraj WYSYŁKA', blank=True, null=True)
    order_note = models.TextField(max_length=1000, verbose_name='Uwagi do zamówienia', blank=True)
    order_total = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Suma')
    status = models.CharField(max_length=12, choices=STATUS, default='Nowe', verbose_name='Status')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False, verbose_name='Czy zamówione?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data zaktualizowania')

    class Meta:
        verbose_name = 'Zamowienie'
        verbose_name_plural = 'Zamowienia'

    def imie_i_nazwisko(self):
        return f'{self.first_name} {self.last_name}'

    def full_shipping_address(self):
        return f'{self.street_shipment}, {self.zipcode_shipment},' \
               f' {self.city_shipment}, {self.country_shipment}'

    def __str__(self):
        return f'{self.order_number}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Zamówienie')
    user = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE, verbose_name='Użytkownik', blank=True, null=True)
    product = models.ForeignKey(Produkt, on_delete=models.CASCADE, verbose_name='Produkt')
    quantity = models.IntegerField(verbose_name='Ilość')
    product_price = models.FloatField(verbose_name='Cena produktu')
    is_ordered = models.BooleanField(default=False, verbose_name='Czy zamówione?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data zaktualizowania')

    class Meta:
        verbose_name = 'Produkt w zamówieniu'
        verbose_name_plural = 'Produkty w zamówieniu'

    def __str__(self):
        return self.product.nazwa
