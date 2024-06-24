from django.shortcuts import render, redirect, get_object_or_404

from django.http import JsonResponse

import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.




def index(request):
    # user = request.user
    # try:
    #     customer = user.customer
    #     return JsonResponse(customer)
    # except Customer.DoesNotExist:
    #     return JsonResponse({'error': 'User has no customer'}, status=404)

    products = Product.objects.all()

    context = {'products':products}
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

def updateCart(request):
    # if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitems = order.orderitem_set.all()

    totalQty = sum(item.qty for item in orderitems)
    totalCost = sum(item.product.price*item.qty for item in orderitems)

    # else:
    #     totalQty = 0

    context = {'totalQty': totalQty, 'totalCost': totalCost}
    return JsonResponse(context)



# #################### to be eedddiitedd ############################
# def updateCartItem(request, pk):
#     customer = request.user.customer
    
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#     # orderitem = order.orderitem_set.all()

#     # return JsonResponse({'sth'})
#     orderitems = OrderItem.objects.filter(order=order)
    
#     one = orderitems.get(id=pk)
#     itemTotal = one.product.price*one.qty
#     itemQty = one.qty

#     # return JsonResponse({'id ':pk, ' customer ': customer.name, ' totalll ': itemTotal, " updated qty: ": itemQty})
#     context = {'itemTotal': itemTotal , 'itemQty':itemQty}
#     return JsonResponse(context)



def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_itemsQty' : 0, 'get_cart_total_items':0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)
 
def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0 , 'get_cart_itemsQty': 0, 'get_cart_total_items' : 0}
    
    context = {'items':items, 'order': order}
    return render(request, 'store/checkout.html', context )

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