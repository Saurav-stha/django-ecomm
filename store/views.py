from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):

    products = Product.objects.all()

    context = {'products':products}
    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html')
 
def checkout(request):
    context = {}
    return render(request, 'store/checkout.html')
