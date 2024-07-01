from django.shortcuts import render, redirect

from django.http import JsonResponse

import json
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *

from .utils import cookieCart, cartData, guestOrder
# Create your views here.

def index(request):
    data = cartData(request)
    cartItemsQty = data['cartItemsQty']

    products = Product.objects.all()

    context = {'products':products, 'cartItemsQty': cartItemsQty}
    return render(request, 'store/store.html', context)

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('store.html')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username= username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request,'Invalid Credentials')


    context = {}
    return render(request, 'store/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('store')


def cart(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItemsQty = data['cartItemsQty']

    context = {'items': items, 'order': order, 'cartItemsQty': cartItemsQty}
    return render(request, 'store/cart.html', context)
 
def checkout(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItemsQty = data['cartItemsQty']
    
    context = {'items':items, 'order': order, 'cartItemsQty': cartItemsQty}
    return render(request, 'store/checkout.html', context )

def updateCart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # .filter checks those items of not complete orders(i.e. not paid orders)
        orderitems = order.orderitem_set.all()

        totalQty = sum(item.qty for item in orderitems)
        totalCost = sum(item.product.price*item.qty for item in orderitems)

    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('cart: ' ,cart)
        order = {'get_cart_total' : 0, 'get_cart_itemsQty' : 0, 'get_cart_total_items':0, 'shipping': False}

        cartItemsQty = order['get_cart_itemsQty']
        # print("qty : ",cartItemsQty)

        for i in cart:
            cartItemsQty += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cartItemsQty)

        totalCost = total
        totalQty = cartItemsQty

    context = {'totalQty': totalQty, 'totalCost': totalCost}
    return JsonResponse(context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('id ',productId, ' action ',action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order= order, product=product)

    if action == 'add':
        orderItem.qty = (orderItem.qty + 1)
    elif action == 'remove':
        orderItem.qty = (orderItem.qty - 1)

    orderItem.save()

    if orderItem.qty <= 0:
        orderItem.delete()

    return JsonResponse('Item was added ', safe=False)# safe=false navayea error like of no-csrftoken


def processOrder(request):
    print("data: ", request.body)
    
    transaction_id = datetime.datetime.now().timestamp()
    try:
        data = json.loads(request.body)
    except:
        print("error in loading json data from the fetch form data")
    # return JsonResponse(data, safe=False)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False)

    else:
        customer, order = guestOrder(request, data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    # for checking no any manipulation done by user
    # print(total)
    # tryTotal = int(order.get_cart_total())
    # print(tryTotal)

    # no get_cart_total() cause @property used above the function
    if total == order.get_cart_total:
        # setting order status to complete
        print("yesss")
        order.complete = True
    else:
        print("no god no noooo")

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer =customer,
            order=order,
            address = data['shipping']['address'],
            city=data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],

        )


    order.save()



    return JsonResponse('payment complete', safe=False)


def userProfile(request):
    total_order_cost = 0
    customer = request.user.customer
    profile = User.objects.get(customer=customer)
    shippingInfos = ShippingAddress.objects.filter(customer=customer)
    orders = Order.objects.filter(customer=customer)
    # # print("total orders: " , orders.count())
    for order in orders:
        total_order_cost += order.get_cart_total
        print("cost: ",order.get_cart_total)

    context = {'profile':profile, 'shippingInfos':shippingInfos, 'orders':orders, 'total_order_cost':total_order_cost}
    return render(request, 'store/profile.html',context)