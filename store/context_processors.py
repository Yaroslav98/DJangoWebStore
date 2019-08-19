
from django.contrib import auth

def getting_user(request):
    user=auth.get_user(request)
    return {'user':user}

def getting_cart_products(request):
    if 'cart' not in request.session:
        products_in_cart=None
        cart_count=None
    else:
        products_in_cart=request.session['cart']
        cart_count=len(request.session['cart'])
    return {'products_in_cart':products_in_cart,
            'cart_count':cart_count}