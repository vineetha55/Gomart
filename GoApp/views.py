import math

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *

# Create your views here.
def index(request):
    cat=tbl_Category.objects.all()
    coun=tbl_Country.objects.all()
    brand=tbl_Brand.objects.all()
    return render(request,"index.html",{"cat":cat,"coun":coun,"brand":brand})

def Admin_login(request):
    return render(request,"Admin_login.html")


def login_check(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user:
        login(request,user)
        return redirect("/Admin_Home/")
    else:
        return redirect("/Gomart_Admin/")

def Admin_Home(request):
    return render(request,"Admin_Home.html")

def country(request):
    d=tbl_Country.objects.all()
    return render(request,"country.html",{"d":d})

def add_country(request):
    if request.method=="POST":
        d=tbl_Country()
        d.name=request.POST.get("country")
        d.status=request.POST.get("status")
        d.save()
        return redirect("/country/")
    else:
        return render(request,"add_country.html")
def brands(request):
    d=tbl_Brand.objects.all()
    return render(request,"brands.html",{"d":d})

def add_brands(request):
    if request.method=="POST":
        d=tbl_Brand()
        d.name=request.POST.get("brands")
        d.status=request.POST.get("status")
        d.save()
        return redirect("/brands/")
    else:
        return render(request,"add_brands.html")

def category(request):
    d=tbl_Category.objects.all()
    return render(request,"category.html",{"d":d})


def add_category(request):
    if request.method=="POST":
        d=tbl_Category()
        d.name=request.POST.get("category")
        d.status=request.POST.get("status")
        d.save()
        return redirect("/category/")
    else:
        return render(request,"add_category.html")


def products(request):
    products=tbl_Product.objects.all()
    return render(request,"products.html",{"products":products})

def add_product(request):
    if request.method=="POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        country_id = request.POST.get('country')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        opening_stock = request.POST.get('opening_stock')
        current_stock = request.POST.get('current_stock')
        product_code = request.POST.get('product_code')
        status = request.POST.get('status')
        image = request.FILES['image']
        fs=FileSystemStorage()
        file=fs.save(image.name,image)
        url=fs.url(file)

        # Create and save a new Product object
        product = tbl_Product(
            name=name,
            description=description,
            price=price,
            country_id=country_id,
            brand_id=brand_id,
            category_id=category_id,
            opening_stock=opening_stock,
            current_stock=current_stock,
            product_code=product_code,
            status=status,
            image=url
        )
        product.save()
        return redirect("/products/")
    else:
        cou=tbl_Country.objects.all()
        cat=tbl_Category.objects.all()
        bran=tbl_Brand.objects.all()
        d = tbl_Product.objects.all().last()
        print(d)

        if d == None:
            pdt_code = 'GM/PD00' + '1'
            print(pdt_code)
        else:
            d1 = d.id
            d2 = d1 + 1
            pdt_code = 'GM/PD00' + str(d2)
            print(pdt_code)
        return render(request,"add_products.html",{"cou":cou,"cat":cat,"bran":bran,"pdt_code":pdt_code})

def show_by_country(request,id):
    d=tbl_Product.objects.filter(country=id)
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    return render(request,"show_by_country.html",{"d":d,"cat":cat,"coun":coun,"brand":brand})

def show_by_brand(request,id):
    d=tbl_Product.objects.filter(brand=id)
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    latest=tbl_Product.objects.all()[:9]
    n=range(2)
    return render(request,"show_by_brand.html",{"d":d,"cat":cat,"coun":coun,"brand":brand,
                                                "latest":latest,"n":n})


def shop_by_category(request,id):
    d=tbl_Product.objects.filter(category=id)
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    return render(request,"shop_by_category.html",{"d":d,"cat":cat,"coun":coun,"brand":brand})


def logout_admin(request):
    logout(request)
    return redirect("/Gomart_Admin/")


def contact(request):
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    return render(request,"contact.html",{"cat":cat,"coun":coun,"brand":brand})

def Login(request):
    return render(request,"Login_new.html")


def save_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        fullname = request.POST.get('fullname')

        # Check if a user with the given email already exists
        user = User.objects.filter(email=email).first()

        # If user does not exist, create a new user
        if not user:
            user = User.objects.create_user(username=username, email=email, password=password)

        signup = tbl_SignUp.objects.create(
            user=user,
            mobile=mobile,
            fullname=fullname,
            email=email,
            password=password,


        )
        return redirect("/Login/")


def check_email(request):
    email = request.GET.get('email', None)
    data = {
        'exists': User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)


def check_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user= tbl_SignUp.objects.filter(email=email,password=password)
        if user:
            us = tbl_SignUp.objects.get(email=email, password=password)
            request.session['userid']=us.id
            print(request.session['userid'])
            return redirect("/HomePage/")
        else:
            return redirect("/Login/")

def HomePage(request):

        r=request.session['userid']

        if r:
            user=tbl_SignUp.objects.get(id=r)
            print(user,"jj")
            cat = tbl_Category.objects.all()
            coun = tbl_Country.objects.all()
            brand = tbl_Brand.objects.all()
            return render(request,"HomePage.html",{"user":user,"cat":cat,"coun":coun,"brand":brand})
        else:
            return redirect("/")

def add_to_wishlist(request,id):
    d=tbl_Wishlist()
    pass

def add_vat_gst(request):
    if request.method=="POST":
        f=tbl_Tax()
        f.country_id=request.POST.get("country")
        f.rate=request.POST.get("rate")
        f.save()
        return redirect("/country/")
    else:
        coun=tbl_Country.objects.all()
        return render(request,"add_vat_gst.html",{"coun":coun})


def view_product_single(request,id):
    single=tbl_Product.objects.get(id=id)
    cat = tbl_Category.objects.all()
    return render(request,"view_product_single.html",{"single":single,"cat":cat})
#
# def add_to_cart(request):
#     try:
#         if request.session['userid']:
#             p_id=request.GET.get("p_id")
#             t_price = request.GET.get("t_price")
#             quantity = request.GET.get("quantity")
#             d = tbl_Product.objects.get(id=p_id)
#             cart=tbl_Cart()
#             cart.product_id=p_id
#             cart.user_id=request.session['userid']
#             cart.quantity=quantity
#             cart.total_price=t_price
#             cart.save()
#             cart_total=tbl_Cart.objects.filter(user=request.session["userid"])
#             c_total=0
#             for i in cart_total:
#                 c_total+=int(math.floor(float(i.total_price)))
#
#
#             redirect_url = reverse('cart',kwargs={'c_total': c_total})
#             return JsonResponse({'redirect_url': redirect_url})
#         else:
#
#             redirect_url = reverse('Login')
#             return JsonResponse({'redirect_url': redirect_url})
#     except:
#         redirect_url = reverse('Login')
#         return JsonResponse({'redirect_url': redirect_url})
def cart_user(request):
    c=tbl_Cart.objects.get(user=request.session["userid"])
    cart_details=tbl_Cart_Products.objects.filter(user=request.session["userid"],cart=c)
    cat = tbl_Category.objects.all()

    return render(request,"cart_user.html",{"cart_details":cart_details,"cat":cat,"c":c})

#
# def add_to_wishlist_single(request):
#     try:
#         if request.session['userid']:
#             p_id=request.GET.get("p_id")
#             t_price = request.GET.get("t_price")
#             quantity = request.GET.get("quantity")
#             d = tbl_Product.objects.get(id=p_id)
#             cart=tbl_Wishlist()
#             cart.product_id=p_id
#             cart.user_id=request.session['userid']
#             cart.quantity=quantity
#             cart.total_price=t_price
#             cart.save()
#
#
#
#             redirect_url = reverse('wishlist')
#             return JsonResponse({'redirect_url': redirect_url})
#         else:
#
#             redirect_url = reverse('Login')
#             return JsonResponse({'redirect_url': redirect_url})
#     except:
#         redirect_url = reverse('Login')
#         return JsonResponse({'redirect_url': redirect_url})


def wishlist(request):
    wish = tbl_Cart.objects.filter(user=request.session["userid"])
    return render(request,"wishlist.html",{"wish":wish})


def all_products(request):
    d=tbl_Product.objects.all()
    cat = tbl_Category.objects.all()
    return render(request,"all_products.html",{"d":d,"cat":cat})


def add_to_cart_products(request,id,price):
    try:
        if request.session['userid']:
            if tbl_Cart.objects.filter(user=request.session['userid']).exists():
                cart = tbl_Cart.objects.get(user=request.session['userid'])
                cart.sub_total+= price
                cart.total+= price
                cart.save()
                c = tbl_Cart_Products()
                c.cart_id = cart.id
                c.product_id = id
                c.quantity = 1
                c.total_price = price
                c.user_id = request.session['userid']
                c.save()
                return redirect("/cart_user/")
            else:

                cart=tbl_Cart()
                cart.user_id = request.session['userid']
                cart.sub_total=price
                cart.total=price
                cart.save()
                c=tbl_Cart_Products()
                c.cart_id=cart.id
                c.product_id = id
                c.quantity = 1
                c.total_price = price
                c.user_id = request.session['userid']
                c.save()
                return redirect("/cart_user/")
        else:
            return redirect("/Login/")
    except:
        return redirect("/Login/")


def signup(request):
    return render(request,"signup.html")

def shop_by_category_user(request,id):
    d = tbl_Product.objects.filter(category=id)
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    return render(request, "shop_by_category_user.html", {"d": d, "cat": cat, "coun": coun, "brand": brand})

def signout_user(request):
    del request.session['userid']
    return redirect("/")

def update_cart_products(request):
    q=request.GET.get("q")
    tp=request.GET.get("tp")
    id=request.GET.get("id")
    c=tbl_Cart_Products.objects.get(id=id)
    c.quantity=q
    c.total_price=tp
    c.save()
    data={}
    data['message']="success"
    return JsonResponse(data)

def update_cart_total(request):
    ts = request.GET.get("ts")
    id = request.GET.get("id")
    c = tbl_Cart.objects.get(id=id)
    c.sub_total = ts
    c.total = ts
    c.save()
    data = {}
    data['message'] = "success"
    return JsonResponse(data)

def checkout(request):
    return render(request,"checkout.html")