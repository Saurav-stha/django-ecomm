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
