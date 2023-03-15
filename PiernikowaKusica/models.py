from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    nazwa_ANG = models.CharField(max_length=100, unique=True)
    url = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Kategorie'

    def __str__(self):
        return self.nazwa

    def get_url(self):
        return reverse('ProductsByCategory', args=[self.url])


class Produkt(models.Model):
    nazwa = models.CharField(max_length=255, unique=True)
    nazwa_ANG = models.CharField(max_length=255)
    url = models.SlugField(max_length=100, unique=True)
    opis = models.TextField(blank=True)
    opis_ANG = models.TextField(blank=True)
    sklad = models.TextField(blank=True)
    sklad_ANG = models.TextField(blank=True)
    cena = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    czas_wysylki = models.IntegerField(validators=[MinValueValidator(0)])
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE, default=None, blank=True)
    zdjecie = models.ImageField(upload_to="uploads")

    class Meta:
        verbose_name_plural = 'Produkty'

    def __str__(self):
        return self.nazwa

    def get_url(self):
        return reverse('OnlineShopProductDetail', args=[self.kategoria.url, self.url])


class PolecaneProdukty(models.Model):
    nazwa = models.CharField(max_length=100)
    produkty = models.ManyToManyField(Produkt, related_name='recommended')

    class Meta:
        verbose_name_plural = 'Polecane produkty'

    def __str__(self):
        return self.nazwa
