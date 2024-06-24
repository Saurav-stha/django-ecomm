from django.shortcuts import render
from django.http import HttpResponse
    

from store.models import Order, OrderItem, User

def check(request):
    # user = request.user

    # return HttpResponse(user)
    # Get the customer
    customer = User.objects.get(username='saurav').customer
    # print(customer)
    # return HttpResponse('nada')

    # Get the current incomplete order for the customer
    order = Order.objects.get(customer=customer, complete=False)

    # List all OrderItems for this order
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        print(item.id, item.product.name, item.qty)

    # oneItem = order_items.get(id=39)
    # print(oneItem.qty)

    return HttpResponse("naddda")