from django.http import HttpResponse
from django.shortcuts import render ,get_object_or_404


from .models import Category, Product



def all_products(request):
    products = Product.products.all()
    return render(request, 'home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    print(product.slug)
    return render(request, '1.html', {'products': product})


def search(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    print(category)
    product = Product.objects.filter(category=category)
    print(product)
    return render(request, 'search.html', {'products': product})