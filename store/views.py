from django.shortcuts import redirect, render
from store.models import Customer,ShippingAdress,OrderItem,Order,Product
import json
import datetime
from django.http import JsonResponse
from . utils import cookieCart, cartData, guestOrder


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    product = Product.objects.all()
    context = {'products':product, 'cartItems':cartItems, 'shipping':False}

    return render(request,'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request,'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request,'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    data = json.loads(request.body)
    transaction_id = data['transactionID']

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
              
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'].replace(',','.'))
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAdress.objects.create(
            customer = customer,
            order = order,
            adress = data['shipping']['adress'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    print('Captura:',data)
    return JsonResponse('payment complete..', safe=False)

def status_order(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request,'store/order_status.html',context)

""" 
gambiarra
def atualiza(request,id):
    idt = Order.objects.get(transaction_id=id)
    url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders/{idt}'
    response = url.json()
    print('status do pedido:',response)
    return response """