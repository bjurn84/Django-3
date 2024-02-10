from django.shortcuts import render
from django.utils import timezone
from .models import Order, Product

def client_orders(request):
    current_user = request.user if request.user.is_authenticated else None
    
    client_orders_7_days = get_client_orders(current_user, 7)
    client_orders_30_days = get_client_orders(current_user, 30)
    client_orders_365_days = get_client_orders(current_user, 365)
    
    context = {
        'client_orders_7_days': get_unique_products(client_orders_7_days),
        'client_orders_30_days': get_unique_products(client_orders_30_days),
        'client_orders_365_days': get_unique_products(client_orders_365_days),
    }
    
    return render(request, 'myapp/client_orders.html', context)

def get_client_orders(user, days):
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=days)
    orders = Order.objects.filter(client=user, date_ordered__range=(start_date, end_date))
    return orders

def get_unique_products(orders):
    unique_products = set()
    for order in orders:
        unique_products.update(order.products.all())
    return unique_products