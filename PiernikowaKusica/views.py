from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import View
from PiernikowaKusica.models import *


class HomePage(View):
    def get(self, request):
        return render(request, 'home.html')


class OnlineShop(View):
    def get(self, request):
        products = Produkt.objects.all()
        paginator = Paginator(products, 24)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        heading = 'Wszystkie produkty'

        return render(
            request,
            'all_products.html',
            context={
                'products': paged_products,
                'heading': heading,
            }
        )


class OnlineShopByCategory(View):
    def get(self, request, category_url):
        active_category = get_object_or_404(Kategoria, url=category_url)
        products = Produkt.objects.filter(kategoria=active_category)
        paginator = Paginator(products, 24)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        return render(
            request,
            'products_by_category.html',
            context={
                'products': paged_products,
                'active_category': active_category
            }
        )


class OnlineShopProductDetail(View):
    def get(self, request, category_url, product_url):
        active_category = get_object_or_404(Kategoria, url=category_url)
        active_product = get_object_or_404(Produkt, url=product_url)

        return render(
            request,
            'online_shop_product_detail.html',
            context={
                'active_product': active_product,
                'active_category': active_category,
            }
        )


class Orders(View):
    def get(self, request):
        return render(request, 'orders.html')


class AboutUs(View):
    def get(self, request):
        return render(request, 'about_us.html')


class Contact(View):
    def get(self, request):
        return render(request, 'contact.html')


class Information(View):
    def get(self, request):
        return render(request, 'information.html')


class Search(View):
    def get(self, request, products=None):
        if 'fraza' in request.GET:
            keyword = request.GET['fraza']
            if keyword:
                products = Produkt.objects.order_by('nazwa').filter(nazwa__icontains=keyword)
        heading = 'Znalezione produkty'
        return render(
            request,
            'all_products.html',
            context={
                'products': products,
                'heading': heading,
            }
        )
