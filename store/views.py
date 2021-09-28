from django.shortcuts import render
from store.models import Customer,ShippingAdress,OrderItem,Order,Product


def store(request):
    product = Product.objects.all()
    context = {'products':product}
    return render(request,'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_total_items':0}

    context = {'items':items, 'order':order}
    return render(request,'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []

    context = {'items':items, 'order':order}
    return render(request,'store/checkout.html', context)