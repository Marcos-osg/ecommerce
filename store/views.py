from django.shortcuts import render
from store.models import Customer,ShippingAdress,OrderItem,Order,Product
import json
import datetime
from django.http import JsonResponse


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_total_items':0}
        cartItems = order['get_total_items']

    product = Product.objects.all()
    context = {'products':product, 'cartItems':cartItems, 'shipping':False}

    return render(request,'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}
        print('cart:',cart)
        items = []
        order = {'get_cart_total':0, 'get_total_items':0}
        cartItems = order['get_total_items']

        for i in cart:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total =(product.price * cart[i]['quantity'])

            order['get_cart_total']+= total
            order['get_total_items']+= cart[i]['quantity']

            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                    'quantity':cart[i]['quantity'],
                    'get_total':total,
            }
            items.append(item)

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shipping':False}
    return render(request,'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_total_items':0, 'shipping':False}
        cartItems = order['get_total_items']

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
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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

    else:
        print('User is not logged in')
    return JsonResponse('payment complete..', safe=False)