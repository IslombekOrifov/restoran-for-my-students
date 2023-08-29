from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from .models import Category, Product, Order, OrderItem
from .card import Cart

def main_menu(request, slug=None):
    cart = Cart(request)
    categories = Category.objects.all()
    if slug is None:
        products = Product.objects.filter(category=categories.first())
        category = None
    else:
        products = Product.objects.filter(category__slug=slug)
        category = categories.filter(slug=slug).first()
    context = {
        'categories': categories,
        'category': category,
        'products': products,
        'cart': cart,
    }
    return render(request, 'products/index.html', context)


def cart_add(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')

    print(product_id)
    product_count = int(request.POST.get('product_count'))
    print(product_count)
    product = get_object_or_404(Product, pk=int(product_id))
    cart.add(product, quantity=product_count)
    return JsonResponse({'status':'ok'})

def cart_remove(request):
    product_id = request.POST.get('product_id')
    cart = Cart(request)
    cart.clear()
    # cart.remove(product_id)
    return JsonResponse({'status':'ok'})


def order_create(request):
    cart = Cart(request)
    order = Order.objects.create(price_all=cart.get_total_price(), waiter=request.user)
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], product_count=item['quantity'])
        product = item['product']
        product.count_sold = product.count_sold + item['quantity']
        product.save()
    cart.clear()
    return redirect("products:main_menu")