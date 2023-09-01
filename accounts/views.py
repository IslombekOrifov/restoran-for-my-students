from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.db.models import Q, F, Subquery, Sum, OuterRef, IntegerField

from .forms import LoginForm, PeriodForm
from .models import CustomUser

from products.models import Order, OrderItem, Product

def login_func(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            print(username)
            password = cd['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:
                    return redirect('accounts:dashboard_admin')
                else:
                    return render("products:main_menu")
            else:
                return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html', {'form': form})


def logout_func(request):
    logout(request)
    return render(request, 'accounts/login1.html')



def dashboard(request):
    order_items = OrderItem.objects.filter(created__month=timezone.now().month, created__day=timezone.now().day).values_list('product__id')
    products = Product.objects.filter(id__in=order_items).annotate(ostatka=F('count_all') - F('count_sold'), foyda=F('price') - F('real_price'), foyda_umumiy=(F('price') - F('real_price'))*F('count_sold'))
    context = {
        'products': products,
    }
    return render(request, 'accounts/admin.html', context)


def dashboard_admin(request):
    session = request.session
    start_date = None
    end_date = None
    form = PeriodForm()
    if request.method == 'POST':
        form = PeriodForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            session['start_date'] = f"{cd['start_date']}"
            session['end_date'] = f"{cd['end_date']}"
            session.modified = True
            start_date = cd['start_date']
            end_date = cd['end_date']

    elif request.method == 'GET':
        if session.get('start_date', False) and session.get('end_date', False):
            start_date = session['start_date']
            end_date = session['end_date']
        else: 
            start_date = timezone.now().date()
            end_date = timezone.now().date()
    # order_items = OrderItem.objects.filter(created__month=timezone.now().month, created__day=timezone.now().day).values_list('product__id')
    # order_items = OrderItem.objects.filter(created__date__gte=start_date, order__waiter__username='admin', created__date__lte=end_date).values_list('product__id')
    # products = Product.objects.filter(id__in=order_items).annotate(
    #     ostatka=F('count_all') - F('count_sold'), 
    #     foyda=F('price') - F('real_price'),
    #     foyda_umumiy=Subquery(OrderItem.objects.filter(
    #         created__date__gte=start_date, created__date__lte=end_date
    #     ).values_list((OuterRef('price') - OuterRef('real_price'))*OuterRef('count_sold')))
    # )
    
    orders_price = Order.objects.filter(created__date__gte=start_date, created__date__lte=end_date).annotate(
        umumiy_tan=Subquery(
        OrderItem.objects.filter(
            order=OuterRef('pk'),
        ).annotate(
            real_price_order=F('product_count') * F('product__real_price')
        ).values('order').annotate(
            real_price=Sum('real_price_order')
        ).values('real_price')[:1]
    )
    ).aggregate(
        umumiy_savdo=Sum('price_all'), 
        tan_narx=Sum('umumiy_tan')
        
    )
    if orders_price['tan_narx']:
        orders_price['umumiy_foyda'] = orders_price['umumiy_savdo'] - orders_price['tan_narx']
    else:
        orders_price['umumiy_foyda'] = 0
    order_items = OrderItem.objects.filter(created__date__gte=start_date, created__date__lte=end_date).values_list('product__id')
    products = Product.objects.filter(id__in=order_items).annotate(
        sotildi=Subquery(
            OrderItem.objects.filter(
                product=OuterRef('pk'),
                created__date__gte=start_date,
                created__date__lte=end_date
            ).values('product').annotate(
                    total_product_count=Sum('product_count')
                ).values('total_product_count')[:1]
        ),
        umumiysavdo=F('sotildi') * F('price'),
    )
    context = {
        'orders_price': orders_price,
        'products': products,
        'form': form,
    }
    
    return render(request, 'accounts/admin1.html', context)

