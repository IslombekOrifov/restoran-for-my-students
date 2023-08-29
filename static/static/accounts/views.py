from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.db.models import Q, F, Subquery

from .forms import LoginForm

from products.models import Order, OrderItem, Product

def login_func(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:
                    return redirect('accounts:dashboard')
                else:
                    return render(request, 'products/index.html')
            else:
                return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


def logout_func(request):
    logout(request)
    return render(request, 'accounts/login.html')



def dashboard(request):
    order_items = OrderItem.objects.filter(created__month=timezone.now().month, created__day=timezone.now().day).values_list('product__id')
    products = Product.objects.filter(id__in=order_items).annotate(ostatka=F('count_all') - F('count_sold'), foyda=F('price') - F('real_price'))
    context = {
        'products': products,
    }
    return render(request, 'accounts/admin.html', context)

