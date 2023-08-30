from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.db.models import Q, F, Subquery, Sum, OuterRef

from .forms import LoginForm, PeriodForm

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
    products = Product.objects.filter(id__in=order_items).annotate(ostatka=F('count_all') - F('count_sold'), foyda=F('price') - F('real_price'), foyda_umumiy=(F('price') - F('real_price'))*F('count_sold'))
    context = {
        'products': products,
    }
    return render(request, 'accounts/admin.html', context)


def dashboard_admin(request):
    session = request.session
    start_date = None
    end_date = None
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
    orders_price = Order.objects.filter(created__date__gte=start_date, created__date__lte=end_date).aggregate(
        jami_savdo=Sum('price_all'), 
    )

    order_items = OrderItem.objects.filter(created__date__gte=start_date, created__date__lte=end_date).values_list('product__id')
    
    products = Product.objects.filter(id__in=order_items).annotate(
        ostatka=F('count_all') - F('count_sold'), 
        foyda=F('price') - F('real_price'),
        foyda_umumiy=Subquery(OrderItem.objects.filter(
            created__date__gte=start_date, created__date__lte=end_date
        ).values_list((OuterRef('price') - OuterRef('real_price'))*OuterRef('count_sold')))
        )
    
    context = {
        'orders_price': orders_price['jami_savdo'],
        'products': products,
    }
    
    return render(request, 'accounts/admin1.html', context)

