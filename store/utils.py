import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('cart: ' ,cart)
    items = []
    order = {'get_cart_total' : 0, 'get_cart_itemsQty' : 0, 'get_cart_total_items':0, 'shipping': False}
    # previous set cart items qty
    cartItemsQty = order['get_cart_itemsQty']

    for i in cart:
        try:

            cartItemsQty += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_itemsQty'] += cart[i]['quantity']


            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'qty':cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    print(items)

    return {'items': items, 'order': order, 'cartItemsQty': cartItemsQty}

def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItemsQty = order.get_cart_total_items
    else:
        items = []
        order = {'get_cart_total': 0 , 'get_cart_itemsQty': 0, 'get_cart_total_items' : 0, 'shipping': False}
        cartData = cookieCart(request)
        items = cartData['items']
        order = cartData['order']
        cartItemsQty = cartData['cartItemsQty']
    return {'items': items, 'order': order, 'cartItemsQty': cartItemsQty}   


def guestOrder(request, data):
    print("User not logged in hai")


    print ("COOKIES: ", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)

    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            qty=item['qty']
        )
    return customer, order