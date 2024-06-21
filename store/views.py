from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.
def index(request):

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
