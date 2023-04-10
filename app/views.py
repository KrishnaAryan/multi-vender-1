from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Max, Min, Sum
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    sliders=slider.objects.all().order_by('-id')
    baner=banner_area.objects.all().order_by('-id')
    main_category=MainCategory.objects.all()
    product=Product.objects.filter(section__name='Top Deal Of The Day')
    context={
        'sliders':sliders,
        'baner':baner,
        'main_category':main_category,
        'product':product
    }
    return render(request, 'main/index.html',context)

def product_detail(request, slug):
    product=Product.objects.filter(slug=slug)
    if product.exists():
         product=Product.objects.filter(slug=slug)
    else:
        return redirect('404')
    context={
        'product':product
    }
    return render(request, 'product/product_detail.html',context)


def error404(request):
    return render(request, 'errors/404.html')

def my_account(request):
    return render(request, 'account/my-account.html')

def user_register(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already exists")
            return redirect('login')
        if User.objects.filter(email=email).exists():
            messages.error(request, "EmailId is already exists")
            return redirect('login')
        
        user=User(
            username=username,
            email=email,
            
        )
        user.set_password('password')
        user.save()
        return redirect('login')
    
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username/Email and Password are Invalid !')
            return redirect('login')

@login_required(login_url='/accounts/login/')        
def profile(request):
    return render(request, 'profile/profile.html')

@login_required(login_url='/accounts/login/')    
def profile_update(request):
    if request.method == "POST":
        usernames=request.POST.get("username")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        user_id=request.user.id
        
        user = User.objects.get(id=user_id)
        user.first_name=first_name
        user.last_name=last_name
        user.usernames=usernames
        if email:
            user.email=email
        if password != None and password !="":
            user.set_password(password)
        user.save()
        messages.success(request, "Profile are successfully Updated..!😊")
        return redirect("profile")


def about(request):
    return render(request, 'main/about.html')

def contactus(request):
    return render(request, 'main/contactus.html')

def product(request):
    category=Category.objects.all()
    product=Product.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    else:
        product = Product.objects.all()

    context={
       'category':category,
       'product':product,
       'min_price':min_price,
       'max_price':max_price,
	   'FilterPrice':FilterPrice,

    }
    return render(request, 'product/product.html', context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()

    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()

    t = render_to_string('ajax/product.html', {'product': allProducts})
    return JsonResponse({'data': t})

def checkout(request):
    return render(request, 'checkout/checkout.html')


@login_required(login_url='/accounts/login/')   
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url='/accounts/login/')   
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url='/accounts/login/')   
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url='/accounts/login/')   
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url='/accounts/login/')   
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url='/accounts/login/')   
def cart_detail(request):
    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)
    
    invalid_coupon=None
    valid_coupon=None
    coupon=None
    if request.method == "GET":
        coupon_code=request.GET.get("coupon_code")
        if coupon_code:
            try:
                coupon= CouponCode.objects.get(code=coupon_code)
                valid_coupon="Are Applicable on Current Order !"
            except:
                invalid_coupon="Invalid Coupon Code"
    context={
        'packing_cost':packing_cost,
        'tax':tax,
        'coupon':coupon,
        'valid_coupon':valid_coupon,
        'invalid_coupon':invalid_coupon,   
        
    }
    return render(request, 'cart/cart.html', context)