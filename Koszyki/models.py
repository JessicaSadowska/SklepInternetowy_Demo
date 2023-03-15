from django.db import models

from Konta.models import Uzytkownik
from PiernikowaKusica.models import Produkt


class Koszyk(models.Model):
    id_koszyka = models.CharField(max_length=250, blank=True)
    data_utworzenia = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id_koszyka

    class Meta:
        verbose_name_plural = 'Koszyki'


class ProduktKoszyka(models.Model):
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE, null=True)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    koszyk = models.ForeignKey(Koszyk, on_delete=models.CASCADE, null=True)
    ilosc = models.IntegerField()
    wartosc = models.DecimalField(max_digits=10, decimal_places=2)
    aktywny = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Produkty w koszyku'

    def __str__(self):
        return self.produkt.nazwa
