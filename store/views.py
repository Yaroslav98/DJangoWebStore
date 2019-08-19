from django.shortcuts import render,redirect
from django.http import JsonResponse
from decimal import *
from django.template.context_processors import csrf
from .models import *
from .forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger


def home(request):
    most_popular_brand=Brand.objects.order_by('sales')[:8]
    most_popular_products = Product.objects.order_by('sales')[:8]

    most_popular_products_image=[most_popular_products[i].productimage_set.get(is_main=True)
                                for i in range (len(most_popular_products))]
    context={'most_popular_brands': most_popular_brand,
             'most_popular_products_image':most_popular_products_image
             }
    print( most_popular_products_image)
    return render(request, 'store/Home.html', context)


def category_view(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, 'store/Categories.html', context)


def product_view(request,product_id):
    product=ProductImage.objects.get(product=product_id)
    return render(request, 'store/Product.html',{'product':product})

def brand_view(request,brand_id):
    products=ProductImage.objects.filter(product__brand=brand_id,is_main=True)[:8]
    brand=Brand.objects.get(id=brand_id)
    return render(request, 'store/Brand.html',{'products':products,'brand':brand})

def brands_view(request):
    brands=Brand.objects.all()
    return render(request,'store/Brands.html',{'brands':brands})

def search_products_filter(product_name,category,brand,minprice,maxprice):
    # all !=not
    if category != 'Not' and brand != 'Not' and minprice != None and maxprice != None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__category__name=category, product__brand__name=brand,
                                               product__price__gte=minprice, product__price__lte=maxprice)

    # category==not   and brand!= not

    elif category == 'Not' and brand != 'Not' and minprice != None and maxprice != None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__brand__name=brand, product__price__gte=minprice,
                                               product__price__lte=maxprice)

    elif category == 'Not' and brand != 'Not' and minprice == None and maxprice != None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__brand__name=brand, product__price__lte=maxprice)

    elif category == 'Not' and brand != 'Not' and minprice != None and maxprice == None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__brand__name=brand, product__price__gte=minprice)

    elif category == 'Not' and brand != 'Not' and minprice == None and maxprice == None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__brand__name=brand)
    # category==not  and brand==not

    elif category == 'Not' and brand == 'Not' and minprice != None and maxprice != None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__price__gte=minprice, product__price__lte=maxprice)

    elif category == 'Not' and brand == 'Not' and minprice == None and maxprice != None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__price__lte=maxprice)

    elif category == 'Not' and brand == 'Not' and minprice != None and maxprice == None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__price__gte=minprice)

    elif category == 'Not' and brand == 'Not' and minprice == None and maxprice == None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name)
    # category!=not and brand==not

    elif category != 'Not' and brand == 'Not' and minprice != None and maxprice != None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__category__name=category, product__price__gte=minprice,
                                               product__price__lte=maxprice)

    elif category != 'Not' and brand == 'Not' and minprice == None and maxprice != None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__category__name=category, product__price__lte=maxprice)

    elif category != 'Not' and brand == 'Not' and minprice != None and maxprice == None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__category__name=category, product__price__gte=minprice)

    elif category != 'Not' and brand == 'Not' and minprice == None and maxprice == None:
        products = ProductImage.objects.filter(is_main=True, product__category__name=category,
                                               product__name__icontains=product_name)

    # category!=not and brand!=not

    elif category != 'Not' and brand != 'Not' and minprice == None and maxprice != None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__brand__name=brand,
                                               product__category__name=category,
                                               product__price__lte=maxprice)

    elif category != 'Not' and brand != 'Not' and minprice != None and maxprice == None:
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name,
                                               product__brand__name=brand,
                                               product__category__name=category,
                                               product__price__gte=minprice)

    elif category != 'Not' and brand != 'Not' and minprice == None and maxprice == None:
        products = ProductImage.objects.filter(is_main=True, product__category__name=category,
                                               product__brand__name=brand, product__name__icontains=product_name)
    return products

def products(request):
    #filter products
    context={}
    if request.GET:
        products = ProductImage.objects.filter(is_main=True)
        if 'product_name' in request.GET:
            product_name = request.GET['product_name']
            #for navbar search
            products = ProductImage.objects.filter(is_main=True,product__name__icontains=product_name)
            if 'category' in request.GET and 'brand' in request.GET and 'minprice' in request.GET and 'maxprice' in request.GET:
                if(request.GET['category']==''):
                    category='Not'
                else:
                    category = request.GET['category']
                if (request.GET['brand'] == ''):
                    brand='Not'
                else:
                    brand = request.GET['brand']
                print(category)
                if request.GET['minprice']=='' or request.GET['minprice']=='None':
                    minprice=None
                else:
                    minprice = Decimal(request.GET['minprice'])
                if request.GET['maxprice']=='' or request.GET['maxprice']=='None':
                    maxprice=None
                else:
                    maxprice = Decimal(request.GET['maxprice'])
                if (maxprice!=None and minprice!=None and minprice > maxprice):
                    return render(request, 'store/search_price_error.html')
                context['saved_product_param'] = product_name
                context['saved_category_param']=category
                context['saved_brand_param']=brand
                context['saved_minprice_param']=minprice
                context['saved_maxprice_param']=maxprice
                products=search_products_filter(product_name,category,brand,minprice,maxprice)

    else:
        products = ProductImage.objects.filter(is_main=True)

    product_paginator=Paginator(products,1)
    page = request.GET.get('page')
    try:
        # Если существует, то выбираем эту страницу
        products_pag= product_paginator.get_page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        products_pag = product_paginator.get_page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        products_pag = product_paginator.get_page(product_paginator.num_pages)
    categories=Category.objects.all()
    brands=Brand.objects.all()
    context['products']=products_pag
    context['categories'] = categories
    context['brands'] = brands
    return render(request,'store/Products.html',context)

def brand_products_view(request,brand_id):
    brand = Brand.objects.get(id=brand_id)
    context={}
    # filter products
    if request.GET:
            if 'product_name' in request.GET and'category' in request.GET and 'minprice' in request.GET and 'maxprice' in request.GET:
                product_name = request.GET['product_name']
                if(request.GET['category']==''):
                    category='Not'
                else:
                    category = request.GET['category']
                if request.GET['minprice'] == '' or request.GET['minprice'] == 'None':
                    minprice = None
                else:
                    minprice = Decimal(request.GET['minprice'])
                if request.GET['maxprice'] == '' or request.GET['maxprice'] == 'None':
                    maxprice = None
                else:
                    maxprice = Decimal(request.GET['maxprice'])

                if (maxprice != None and minprice != None and minprice > maxprice):
                    return render(request, 'store/search_price_error.html')
                context['saved_product_param'] = product_name
                context['saved_category_param'] = category
                context['saved_minprice_param'] = minprice
                context['saved_maxprice_param'] = maxprice
                products = search_products_filter(product_name, category, brand, minprice, maxprice)

    else:
        products = ProductImage.objects.filter(is_main=True,product__brand=brand)
    product_paginator = Paginator(products, 1)
    page = request.GET.get('page')
    try:
        # Если существует, то выбираем эту страницу
        products_pag = product_paginator.get_page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        products_pag = product_paginator.get_page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        products_pag = product_paginator.get_page(product_paginator.num_pages)
    context['products'] = products_pag
    context['categories'] = Category.objects.all()
    context['brand']=brand
    return render(request, 'store/Brand_products.html', context)


def category_products_view(request,category_id):
    category = Category.objects.get(id=category_id)
    context={}
    # filter products
    if request.GET:
            if  'product_name' in request.GET and 'brand' in request.GET and 'minprice' in request.GET and 'maxprice' in request.GET:
                product_name = request.GET['product_name']
                if (request.GET['brand'] == ''):
                    brand='Not'
                else:
                    brand = request.GET['brand']

                if request.GET['minprice'] == '' or request.GET['minprice'] == 'None':
                    minprice = None
                else:
                    minprice = Decimal(request.GET['minprice'])
                if request.GET['maxprice'] == '' or request.GET['maxprice'] == 'None':
                    maxprice = None
                else:
                    maxprice = Decimal(request.GET['maxprice'])
                context['saved_product_param'] = product_name
                context['saved_brand_param']=brand
                context['saved_minprice_param']=minprice
                context['saved_maxprice_param']=maxprice
                products = search_products_filter(product_name, category, brand, minprice, maxprice)

    else:
        products = ProductImage.objects.filter(is_main=True,product__category=category)
    product_paginator = Paginator(products, 1)
    page = request.GET.get('page')
    try:
        # Если существует, то выбираем эту страницу
        products_pag = product_paginator.get_page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        products_pag = product_paginator.get_page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        products_pag = product_paginator.get_page(product_paginator.num_pages)
    brands=Brand.objects.all()
    context['products'] = products_pag
    context['category'] = category
    context['brands'] = brands
    return render(request, 'store/Category_products.html', context)

def registration_view(request):
    context={}
    context.update(csrf(request))
    context['regform']= UserForm()
    if request.POST:
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            user=User.objects.get(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password1'])
            user.userinfo.phonenumber=request.POST['phone_number']
            user.save()
            newuser=auth.authenticate(username=form.cleaned_data['username'],
                                      password=form.cleaned_data['password1'])
            auth.login(request,newuser)
            return redirect('/')
        else:
            context['regform']=form
            return render(request,'store/Registration.html',context)
    return render(request,'store/Registration.html',context)


def login_view(request):
    context={}
    context.update(csrf(request))
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        elif user is None:
            context['error_message']='Wrong login or password'
            return render(request, 'store/Login.html', context)
    else:
        return render(request, 'store/Login.html', context)


def logout_view(request):
    auth.logout(request)
    return redirect('/')

def account_orders_view(request):
    context = {}
    user=auth.get_user(request)
    context['user']=user
    context['orders']=Order.objects.filter(user=user.id)
    return render(request, 'store/Account_orders.html', context)


def account_info_view(request):
    context = {}
    context["user_info"]=UserInfo.objects.get(user=auth.get_user(request).id)

    return render(request, 'store/Account_info.html', context)


def account_info_edit_view(request):
    context = {}
    context.update(csrf(request))
    if request.POST:
        user = User.objects.get(id=auth.get_user(request).id)
        user.userinfo.info=request.POST['information']
        user.userinfo.phonenumber=request.POST['phone_number']
        if 'user_photo' in request.FILES:
            uploaded_file=request.FILES['user_photo']
            user.userinfo.photo=uploaded_file
        user.save()
    return render(request, 'store/Account_info_edit.html', context)


def order_info_view(request,order_id):
    context = {}
    order=Order.objects.get(id=order_id)
    if order.user==auth.get_user(request):
        context["order"]=order
        context["products_in_order"]=ProductInOrder.objects.filter(order=order_id)
        return render(request, 'store/Order_info.html', context)
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")

def add_product_in_cart(request):
    product_id=int(request.POST.get("product_id",None))
    count=int(request.POST.get("product_count",None))
    product=Product.objects.get(id=product_id)
    product_id=str(product_id)
    product_image=ProductImage.objects.get(product=product,is_main=True)
    image=str(product_image.image.url)
    returndict = {}
    if 'cart' not in request.session:
        request.session['cart']={}
    if product_id not in request.session['cart']:
        request.session['cart'][product_id]={'name':product.name,
                                             'count':count,
                                             'price':int(product.price)*count,
                                             'image':image,
                                             }
        request.session.save()
        returndict=request.session['cart'][product_id]
        returndict["product_id"] = product_id
        returndict["cart_count"] = str(len(request.session['cart']))
    else:
        oldcount=request.session['cart'][product_id]['count']
        request.session['cart'][product_id]['count']=oldcount+count
        newcount=request.session['cart'][product_id]['count']
        request.session['cart'][product_id]['price']=int(product.price)*newcount
        request.session.save()

        returndict = request.session['cart'][product_id]
        returndict["product_id"] = str(product_id)
        returndict["cart_count"]=str(len(request.session['cart']))
    print(returndict)
    return JsonResponse(returndict)


def remove_from_cart(request):
    product_id=request.POST.get("product_id",None)
    request.session['cart'].pop(product_id)
    request.session.save()
    returndict={"cart_count":str(len(request.session['cart']))}
    return  JsonResponse(returndict)


def creating_order(request):
    context={}
    context.update(csrf(request))
    context['products_in_cart']=request.session['cart']
    if request.POST:
        order=Order.objects.create(user=auth.get_user(request))
        for product_id,product_info in request.session['cart'].items():
            ProductInOrder.objects.create(product_id=product_id,count=product_info["count"],
                                          price=product_info["price"],order=order)
        request.session['cart'].clear()
        return render(request, 'store/Creating_order.html', context)
    else:
        return render(request, 'store/Creating_order.html', context)

def dynamic_search(request):
    return_data ={}
    if request.GET:
        product_name = request.GET['search_text']
        products = ProductImage.objects.filter(is_main=True, product__name__icontains=product_name)[:4]
        for product in products:
            imageurl=str(product.image.url)
            return_data[product.product.id]={
                "product_image_url":imageurl,
                "name":product.product.name,
                "rate":product.product.rate,
                "price":product.product.price}
    return JsonResponse(return_data)

@login_required()
def creating_review(request,product_id):
    context={}
    context.update(csrf(request))
    product=Product.objects.get(id=product_id)
    user=auth.get_user(request)
    review_exist=ProductReview.objects.filter(product=product,user=user).exists()
    context["product"]=product
    if request.POST:
        if "rate" in  request.POST and "text" in request.POST:
            rate=request.POST["rate"]
            text=request.POST["text"]
            if review_exist==True:
                ProductReview.objects.update(product=product, user=user, rating=rate, text=text)
                print('update')
            elif review_exist==False:
                ProductReview.objects.create(product=product,user=user,rating=rate,text=text)
                print('create')
    if review_exist==True:
        review = ProductReview.objects.get(product=product, user=user)
        context["review_info"] = review
        if review.rating == 1:
            context["radio_1"] = True
        if review.rating == 2:
            context["radio_2"] = True
        if review.rating == 3:
            context["radio_3"] = True
        if review.rating == 4:
            context["radio_4"] = True
        if review.rating == 5:
            context["radio_5"] = True
    return render(request,'store/Creating_review.html',context)

def product_reviews(request,product_id):
    context={}
    reviews = ProductReview.objects.filter(product=product_id)
    product = Product.objects.get(id=product_id)
    context["product"]=product
    context['reviews']=reviews
    return render(request,'store/Product_reviews.html',context)
