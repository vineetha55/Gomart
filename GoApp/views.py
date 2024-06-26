import json

from datetime import date, datetime
from django.core.mail import EmailMessage

from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache

import requests
import stripe as stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

from .models import *

def sample(request):
    return render(request, "sample.html")
# Create your views here.
def index(request):
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    best = tbl_Product.objects.filter(best_score__gte=10)
    prod = tbl_Product.objects.all()
    deal = tbl_Deals.objects.filter(status="Start")
    post1 = tbl_poster1.objects.get()
    post2 = tbl_poster2.objects.get()
    post3 = tbl_poster3.objects.get()
    post4 = tbl_poster4.objects.get()
    post5 = tbl_poster5.objects.get()
    post6 = tbl_poster6.objects.get()
    post7 = tbl_poster7.objects.get()
    new_pdt = tbl_Product.objects.all().order_by('-id')[:3]
    organic = tbl_Product.objects.all()[:3]
    veg = tbl_Product.objects.filter(category__name="Vegetables")
    meat = tbl_Product.objects.filter(category__name="Meats")
    return render(request, "index.html",
                  {"cat": cat, "coun": coun, "brand": brand, "best": best,
                   "prod": prod, "deal": deal, "post1": post1,
                   "post2": post2, "post3": post3, "post4": post4,
                   "post5": post5, "post6": post6, "post7": post7,
                   "new_pdt": new_pdt, "organic": organic, "veg": veg, "meat": meat})


def Admin_login(request):
    return render(request, "Admin_login.html")


def login_check(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return redirect("/Admin_Home/")
    else:
        return redirect("/Gomart_Admin/")


@never_cache
def Admin_Home(request):
    current_date=date.today()
    comp_orders=tbl_Checkout.objects.filter(status="Completed")
    pend_orders=tbl_Checkout.objects.filter(status="Pending")
    deli_now=tbl_Checkout.objects.filter(status="Delivery")
    today_orders=tbl_Checkout.objects.filter(created_at=current_date)
    return render(request, "Admin_Home.html")

def change_password_owner(request):
    data=tbl_admin_login.objects.get()
    return render(request,"change_password_owner.html",{"data":data})

def update_password(request):
    n_password = request.POST.get("new_pass")
    password=request.POST.get("old_pass")
    user=authenticate(request,username="gomart",password=password)
    print(user)
    user.set_password(n_password)
    user.save()
    d = tbl_admin_login.objects.get()
    d.password = request.POST.get("new_pass")
    d.save()
    messages.success(request,"Password Changed successfully")
    return redirect("/Admin_Home/")
@never_cache
def country(request):
    d = tbl_Country.objects.all()
    return render(request, "country.html", {"d": d})


@never_cache
def add_country(request):
    if request.method == "POST":
        d = tbl_Country()
        d.name = request.POST.get("country")
        d.status = request.POST.get("status")
        d.save()
        return redirect("/country/")
    else:
        return render(request, "add_country.html")

def edit_country(request,id):
    if request.method=="POST":
        d = tbl_Country.objects.get(id=id)
        d.name=request.POST.get("country")
        d.status = request.POST.get("status")
        d.save()
        return redirect("/country/")

    else:
        d=tbl_Country.objects.get(id=id)
        return render(request,"edit_country.html",{"d":d})

def delete_country(request,id):
    data=tbl_Country.objects.get(id=id)
    print(data)
    data.delete()
    return redirect("/country/")
@never_cache
def brands(request):
    d = tbl_Brand.objects.all()
    return render(request, "brands.html", {"d": d})


@never_cache
def add_brands(request):
    if request.method == "POST":
        d = tbl_Brand()
        d.name = request.POST.get("brands")
        d.status = request.POST.get("status")
        image = request.FILES['image']
        fs = FileSystemStorage()
        file = fs.save(image.name, image)
        url = fs.url(file)
        d.image = url
        d.save()
        return redirect("/brands/")
    else:
        return render(request, "add_brands.html")


@never_cache
def category(request):
    d = tbl_Category.objects.all()
    return render(request, "category.html", {"d": d})


@never_cache
def add_category(request):
    if request.method == "POST":
        d = tbl_Category()
        d.name = request.POST.get("category")
        d.status = request.POST.get("status")
        image = request.FILES['image']
        fs = FileSystemStorage()
        file = fs.save(image.name, image)
        url = fs.url(file)
        d.image = url
        d.save()
        return redirect("/category/")
    else:
        return render(request, "add_category.html")


@never_cache
def products(request):
    products = tbl_Product.objects.all()
    return render(request, "products.html", {"products": products})


@never_cache
def add_product(request):
    if request.method == "POST":
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
        fs = FileSystemStorage()
        file = fs.save(image.name, image)
        url = fs.url(file)
        gross_total = request.POST.get("gross_total")
        weight = request.POST.get("weight")
        weight_measure = request.POST.get("weight_measure")
        tax_rate = request.POST.get("tax_rate")
        tax_amount = request.POST.get("tax_amount")

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
            image=url,
            gross_total=gross_total,
            product_weight=weight,
            product_measure=weight_measure,
            tax_rate=tax_rate,
            tax_amount=tax_amount,

        )
        product.save()
        sub = tbl_Subscribe.objects.all()
        for i in sub:
            send_mail("New Product Alert",
                      "Hi customer We have added a new product in our store please check it and buy it",
                      settings.EMAIL_HOST_USER, [i.email])
        return redirect("/products/")
    else:
        cou = tbl_Country.objects.all()
        cat = tbl_Category.objects.all()
        bran = tbl_Brand.objects.all()
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
        return render(request, "add_products.html", {"cou": cou, "cat": cat, "bran": bran, "pdt_code": pdt_code})


@never_cache
def show_by_country(request, id):
    d = tbl_Product.objects.filter(country=id)
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    return render(request, "show_by_country.html", {"d": d, "cat": cat, "coun": coun, "brand": brand})


def show_by_brand(request, id):
    d = tbl_Product.objects.filter(brand=id)
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    latest = tbl_Product.objects.all()[:9]
    n = range(2)
    return render(request, "show_by_brand.html", {"d": d, "cat": cat, "coun": coun, "brand": brand,
                                                  "latest": latest, "n": n})


def shop_by_category(request, id):
    d = tbl_Product.objects.filter(category=id).order_by("-price")
    c = tbl_Category.objects.get(id=id)
    cat = tbl_Category.objects.all()
    brand = tbl_Brand.objects.all()

    p_count = d.count()
    paginator = Paginator(d, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Determine the range of page numbers to display
    start_page = max(page_obj.number - 2, 1)
    end_page = min(page_obj.number + 2, paginator.num_pages)
    page_range = range(start_page, end_page + 1)
    print(page_range)
    d = page_obj.object_list

    return render(request, "shop_by_category.html", {"d": d, "cat": cat, "p_count": p_count, 'page_obj': page_obj,
                                                     'page_range': page_range, "brand": brand, "c": c})


def logout_admin(request):
    logout(request)
    return redirect("/Gomart_Admin/")


def contact(request):
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    return render(request, "contact.html", {"cat": cat, "coun": coun, "brand": brand})


def Login(request):
    return render(request, "Login_new.html")


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
            user = User.objects.create_user(username=fullname, email=email, password=password)

            signup = tbl_SignUp.objects.create(
                user=user,
                mobile=mobile,
                fullname=fullname,
                email=email,
                password=password,

            )
            messages.success(request,"Successfully Registered Please Login.")
            return redirect("/Login/")
        else:
            messages.error(request,"You are already registered with this email id")
            return redirect("/signup/")




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
        user = tbl_SignUp.objects.filter(email=email, password=password)
        if user:
            us = tbl_SignUp.objects.get(email=email, password=password)
            request.session['userid'] = us.id
            return redirect("/HomePage/")
        else:
            messages.error(request, "Invalid Credentials Please check the email or password")
            return redirect("/Login/")


@never_cache
def HomePage(request):
    try:

        r = request.session['userid']

        if r:
            user = tbl_SignUp.objects.get(id=r)
            print(user, "jj")
            cat = tbl_Category.objects.all()
            coun = tbl_Country.objects.all()
            brand = tbl_Brand.objects.all()
            best = tbl_Product.objects.filter(best_score__gte=10)
            prod = tbl_Product.objects.all()
            deal = tbl_Deals.objects.filter(status="Start")
            post1 = tbl_poster1.objects.get()
            post2 = tbl_poster2.objects.get()
            post3 = tbl_poster3.objects.get()
            post4 = tbl_poster4.objects.get()
            post5 = tbl_poster5.objects.get()
            post6 = tbl_poster6.objects.get()
            post7 = tbl_poster7.objects.get()
            new_pdt = tbl_Product.objects.all().order_by('-id')[:3]
            organic = tbl_Product.objects.all()[:3]
            veg = tbl_Product.objects.filter(category__name="Vegetables")
            meat = tbl_Product.objects.filter(category__name="Meats")

            return render(request, "HomePage.html",
                          {"user": user, "cat": cat, "coun": coun, "brand": brand, "best": best,
                           "prod": prod, "deal": deal, "post1": post1,
                           "post2": post2, "post3": post3, "post4": post4,
                           "post5": post5, "post6": post6, "post7": post7,
                           "new_pdt": new_pdt, "organic": organic, "veg": veg, "meat": meat})
        else:
            return redirect("/")
    except:
        return redirect("/")


@never_cache
def add_to_wishlist(request, id):
    try:
        if request.session['userid']:
            print("hi")
            d = tbl_Product.objects.get(id=id)
            wish = tbl_Wishlist()
            wish.product_id = id
            wish.user_id = request.session['userid']
            wish.save()
            return redirect("/wishlist/")
        else:
            print("hii")

            return redirect("/Login/")
    except:
        print("hiii")
        return redirect("/Login/")


def add_vat_gst(request):
    if request.method == "POST":
        f = tbl_Tax()
        f.country_id = request.POST.get("country")
        f.rate = request.POST.get("rate")
        f.save()
        return redirect("/country/")
    else:
        coun = tbl_Country.objects.all()
        return render(request, "add_vat_gst.html", {"coun": coun})


def view_product_single(request, id):
    try:
        single = tbl_Product.objects.get(id=id)
        cat = tbl_Category.objects.all()

        interest = tbl_Product.objects.filter(category=single.category.id).exclude(id=id)

        return render(request, "view_product_single.html", {"single": single, "cat": cat, "interest": interest})
    except:
        single = tbl_Product.objects.get(id=id)
        cat = tbl_Category.objects.all()
        return render(request, "view_product_single.html", {"single": single, "cat": cat})


@never_cache
def cart_user(request):
    try:
        c = tbl_Cart.objects.get(user=request.session["userid"])
        cart_details = tbl_Cart_Products.objects.filter(user=request.session["userid"], cart=c)
        cat = tbl_Category.objects.all()

        return render(request, "cart_user.html", {"cart_details": cart_details, "cat": cat, "c": c})
    except:
        cat = tbl_Category.objects.all()
        return render(request, "cart_user.html", {"cat": cat})


@never_cache
def wishlist(request):
    wish = tbl_Wishlist.objects.filter(user=request.session["userid"])
    return render(request, "wishlist.html", {"wish": wish})


def all_products(request):
    d = tbl_Product.objects.all()
    d2 = tbl_Product.objects.all()
    cat = tbl_Category.objects.all()
    p_count = d2.count()
    paginator = Paginator(d2, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Determine the range of page numbers to display
    start_page = max(page_obj.number - 2, 1)
    end_page = min(page_obj.number + 2, paginator.num_pages)
    page_range = range(start_page, end_page + 1)
    print(page_range)
    d = page_obj.object_list

    return render(request, "all_products.html", {"d": d, "cat": cat, "p_count": p_count, 'page_obj': page_obj,
                                                 'page_range': page_range, })


@never_cache
def add_to_cart_products(request, id, price):
    try:
        if request.session['userid']:
            if tbl_Cart.objects.filter(user=request.session['userid']).exists():
                cart = tbl_Cart.objects.get(user=request.session['userid'])
                s = cart.sub_total
                s += float(price)
                cart.sub_total = round(s, 2)
                t = cart.total
                t += float(price)
                cart.total = round(t, 2)
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

                cart = tbl_Cart()
                cart.user_id = request.session['userid']
                cart.sub_total = price
                cart.total = price
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
            return redirect("/Login/")
    except:
        return redirect("/Login/")


@never_cache
def add_to_cart_products_single(request, id, price, q):
    try:
        if request.session['userid']:
            if tbl_Cart.objects.filter(user=request.session['userid']).exists():
                cart = tbl_Cart.objects.get(user=request.session['userid'])
                s = int(cart.sub_total)
                s += int(price)
                cart.sub_total = s
                t = int(cart.total)
                t += int(price)
                cart.total = t
                cart.save()
                c = tbl_Cart_Products()
                c.cart_id = cart.id
                c.product_id = id
                c.quantity = q
                c.total_price = price
                c.user_id = request.session['userid']
                c.save()
                return redirect("/cart_user/")
            else:

                cart = tbl_Cart()
                cart.user_id = request.session['userid']
                cart.sub_total = price
                cart.total = price
                cart.save()
                c = tbl_Cart_Products()
                c.cart_id = cart.id
                c.product_id = id
                c.quantity = q
                c.total_price = price
                c.user_id = request.session['userid']
                c.save()
                return redirect("/cart_user/")
        else:
            return redirect("/Login/")
    except:
        return redirect("/Login/")


def signup(request):
    return render(request, "signup.html")


@never_cache
def shop_by_category_user(request, id):
    try:
        ic = request.session['userid']
        d = tbl_Product.objects.filter(category=id)
        table_count = tbl_Product.objects.filter(category=id).count()
        cat = tbl_Category.objects.all()
        coun = tbl_Country.objects.all()
        brand = tbl_Brand.objects.all()
        c = tbl_Category.objects.get(id=id)
        return render(request, "shop_by_category_user.html", {"d": d, "cat": cat, "coun": coun, "brand": brand,
                                                              "table_count": table_count,"c":c})
    except:
        return redirect("/Login/")


def signout_user(request):
    del request.session['userid']
    return redirect("/")


def update_cart_products(request):
    q = request.GET.get("q")
    tp = request.GET.get("tp")
    id = request.GET.get("id")
    c = tbl_Cart_Products.objects.get(id=id)
    c.quantity = q
    c.total_price = tp
    c.save()
    data = {}
    data['message'] = "success"
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


@never_cache
def checkout(request):
    try:
        ic = request.session['userid']

        ship = tbl_Shipment_Address.objects.filter(user=request.session['userid']).last()

        bill = tbl_Billing_Address.objects.filter(user=request.session['userid']).last()
        f = tbl_Cart.objects.get(user=request.session['userid'])
        total_items = tbl_Cart_Products.objects.filter(cart=f).count()

        item_price = f.sub_total
        if float(f.total) >= 50:
            ship_charge = 0
            total_after_ship = f.total
        else:
            # if ship:
            #     eircode=ship.Eircode
            #     # Replace with the desired Eircode
            #     latitude, longitude = get_location_from_eircode(eircode)
            #     if latitude and longitude:
            #         print("Latitude:", latitude)
            #         print("Longitude:", longitude)
            #     else:
            #         print("Location not found or error occurred")
            #     address = get_address_from_coordinates(latitude, longitude)
            #     if address:
            #         print("Address:", address)
            #         ship_charge = 4.95
            #         total_after_ship = f.total
            #
            #     else:
            #         print("Address not found or error occurred")

            ship_charge = 4.95
            tas = float(f.total) + ship_charge
            total_after_ship = round(tas, 2)
        context = {}

        context['total_items'] = total_items
        context['item_price'] = item_price
        context['ship_charge'] = ship_charge
        context['total_after_ship'] = total_after_ship
        context['d'] = ship
        context['bill'] = bill

        return render(request, "checkout.html", context)
    except:
        return render(request, "checkout.html")


@never_cache
def get_address_from_coordinates(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
    headers = {'User-Agent': 'YourApp/1.0'}  # Replace 'YourApp/1.0' with your own user agent string
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'display_name' in data:
            address = data['display_name']
            return address
        else:
            return None
    else:
        print("Error:", response.status_code)
        return None


def get_location_from_eircode(eircode):
    url = f"https://nominatim.openstreetmap.org/search?q={eircode}&format=json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}  # Replace 'YourApp/1.0' with your own user agent string
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("hii")
        data = response.json()
        print(data)
        if data:
            print("hello")
            # Extracting latitude and longitude from the response
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
        else:
            return None, None
    else:
        print("Error:", response.status_code)
        return None, None


def about(request):
    brand = tbl_Brand.objects.all()
    return render(request, "about.html", {"brand": brand})


def save_ship_address(request):
    data = tbl_Shipment_Address()
    data.first_name = request.POST.get("firstname")
    data.last_name = request.POST.get("lastname")
    data.email = request.POST.get("email")
    data.mobile = request.POST.get("mobile")
    data.state = request.POST.get("state")
    data.street_address = request.POST.get("street")
    data.user_id = request.session['userid']
    data.Eircode = request.POST.get("eircode")
    data.save()
    return redirect("checkout1", id=data.id)


@never_cache
def checkout1(request, id):
    try:
        d = tbl_Shipment_Address.objects.get(id=id)
        f = tbl_Cart.objects.get(user=request.session['userid'])
        total_items = tbl_Cart_Products.objects.filter(cart=f).count()
        item_price = f.sub_total
        if float(f.total) >= 50:
            ship_charge = 0
            total_after_ship = f.total
        else:

            ship_charge = 4.95
            tas = float(f.total) + ship_charge
            total_after_ship = round(tas, 2)

        context = {}

        context['total_items'] = total_items
        context['item_price'] = item_price
        context['ship_charge'] = ship_charge
        context['total_after_ship'] = total_after_ship
        context['d'] = d

        return render(request, "checkout.html", context)
    except:
        return render(request, "checkout.html")


def save_bill_address(request):
    if request.method == "POST":
        data = tbl_Billing_Address()
        data.first_name = request.POST.get("firstname")
        data.last_name = request.POST.get("lastname")
        data.email = request.POST.get("email")
        data.mobile = request.POST.get("mobile")
        data.state = request.POST.get("state")
        data.street_address = request.POST.get("street")
        data.user_id = request.session['userid']
        data.Eircode = request.POST.get("eircode")
        data.save()
        return redirect("/checkout/")
    else:
        data = tbl_Billing_Address()
        data.first_name = request.GET.get("fname")
        data.last_name = request.GET.get("lname")
        data.email = request.GET.get("email")
        data.mobile = request.GET.get("mobile")
        data.state = request.GET.get("state")
        data.street_address = request.GET.get("s_address")
        data.user_id = request.session['userid']
        data.Eircode = request.GET.get("eircode")
        data.save()
        return JsonResponse(data={"msg": "success"})


import random
import string


# Function to generate a random order ID
def generate_order_id(length):
    return ''.join(random.choices(string.digits, k=length))


# Function to generate a random invoice number
def generate_invoice_number(length):
    return ''.join(random.choices(string.digits, k=length))


# Function to check if order ID already exists
def order_id_exists(order_id):
    return tbl_Checkout.objects.filter(orderid=order_id).exists()


# Function to check if invoice number already exists
def invoice_number_exists(invoice_number):
    return tbl_Checkout.objects.filter(invoice_number=invoice_number).exists()


# def paymenthandler(request):
#     print("jiii")
#     price=request.POST.get("total_after_ship")
#
#     razorpay_order_id = request.POST.get('order_id')
#
#     payment_id = request.POST.get('payment_id', '')
#     print('paymentid:', str(payment_id))
#
#     signature = request.POST.get('razorpay_signature', '')
#
#     params_dict = {
#         'razorpay_order_id': razorpay_order_id,
#         'razorpay_payment_id': payment_id,
#         'razorpay_signature': signature
#     }
#
#     # verify the payment signature.
#
#     print("res:")
#     amount = int(price) * 100  # Rs. 200
#     razorpay_client.payment.capture(payment_id, amount)
#
#     #checkout saving and stock reduce
#     ca=tbl_Cart.objects.get(user=request.session['userid'])
#     ca_pd=tbl_Cart_Products.objects.filter(cart=ca)
#     order_id = generate_order_id(6)
#     invoice_number = generate_invoice_number(6)
#
#     # Check if order ID and invoice number already exist
#     while order_id_exists(order_id):
#         order_id = generate_order_id(6)
#
#     while invoice_number_exists(invoice_number):
#         invoice_number = generate_invoice_number(6)
#
#     data=tbl_Checkout()
#     data.user_id=request.session['userid']
#     data.item_price=request.POST.get("item_price")
#     data.total_items=request.POST.get("total_items")
#     data.ship_charge=request.POST.get("ship_charge")
#     data.total_after_ship=request.POST.get("total_after_ship")
#     data.discount=request.POST.get("discount")
#     d = request.POST.get("ship")
#     d1 = tbl_Shipment_Address.objects.get(id=d)
#     data.ship_address_id = d1.id
#     data.status="Pending"
#     data.payment_method = "Online"
#     data.orderid=order_id
#     data.invoice_number=invoice_number
#     data.save()
#     for i in ca_pd:
#         data1=tbl_checkout_products()
#         data1.user_id=request.session['userid']
#         data1.checkout_id=data.id
#         data1.product_id=i.product.id
#         data1.quantity=i.quantity
#         data1.total_price=i.total_price
#         data1.save()
#     for j in ca_pd:
#         product=j.product.id
#         quantity=j.quantity
#         table=tbl_Product.objects.get(id=product)
#         stock=table.opening_stock - int(quantity)
#         table.current_stock=stock
#         table.save()
#
#
#     tbl_Cart.objects.get(user=request.session['userid']).delete()
#     print("hiii")
#     return redirect("payment_success",id=data.id)

@never_cache
def all_products_user(request):
    try:
        d = tbl_Product.objects.all()
        d2 = tbl_Product.objects.all()
        cat = tbl_Category.objects.all()
        p_count = d2.count()
        paginator = Paginator(d2, 6)  # 6 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Determine the range of page numbers to display
        start_page = max(page_obj.number - 2, 1)
        end_page = min(page_obj.number + 2, paginator.num_pages)
        page_range = range(start_page, end_page + 1)
        print(page_range)
        d = page_obj.object_list

        return render(request, "all_products_user.html", {"d": d, "cat": cat, "p_count": p_count, 'page_obj': page_obj,
                                                          'page_range': page_range, })
    except:
        return redirect("/Login/")


def all_product_user_sort(request):
    d = tbl_Product.objects.all().order_by('price')
    cat = tbl_Category.objects.all()
    return render(request, "all_products_user.html", {"d": d, "cat": cat})


def all_products_sort(request):
    d = tbl_Product.objects.all().order_by('price')
    cat = tbl_Category.objects.all()
    return render(request, "all_products.html", {"d": d, "cat": cat})


def shop_by_category_sort(request, id):
    d = tbl_Product.objects.filter(category=id).order_by('price')
    c = tbl_Category.objects.get(id=id)
    cat = tbl_Category.objects.all()
    brand = tbl_Brand.objects.all()

    p_count = d.count()
    paginator = Paginator(d, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Determine the range of page numbers to display
    start_page = max(page_obj.number - 2, 1)
    end_page = min(page_obj.number + 2, paginator.num_pages)
    page_range = range(start_page, end_page + 1)
    print(page_range)
    d = page_obj.object_list

    return render(request, "shop_by_category.html", {"d": d, "cat": cat, "p_count": p_count, 'page_obj': page_obj,
                                                     'page_range': page_range, "brand": brand, "c": c})

def shop_by_category_user_sort(request, id):
    d = tbl_Product.objects.filter(category=id).order_by('price')
    c = tbl_Category.objects.get(id=id)
    cat = tbl_Category.objects.all()
    brand = tbl_Brand.objects.all()

    p_count = d.count()
    paginator = Paginator(d, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Determine the range of page numbers to display
    start_page = max(page_obj.number - 2, 1)
    end_page = min(page_obj.number + 2, paginator.num_pages)
    page_range = range(start_page, end_page + 1)
    print(page_range)
    d = page_obj.object_list

    return render(request, "shop_by_category_user.html", {"d": d, "cat": cat, "p_count": p_count, 'page_obj': page_obj,
                                                     'page_range': page_range, "brand": brand, "c": c})

@never_cache
def my_account(request):
    try:
        if request.session['userid']:

            cat = tbl_Category.objects.all()
            my = tbl_SignUp.objects.get(id=request.session['userid'])
            ship = tbl_Shipment_Address.objects.filter(user=request.session['userid'])
            bill = tbl_Billing_Address.objects.filter(user=request.session['userid'])
            recent_orders = tbl_Checkout.objects.filter(user=request.session['userid']).order_by('-id')[:6]

            return render(request, "my_account.html", {"cat": cat, "my": my, "ship": ship, "bill": bill,
                                                       "recent_orders": recent_orders})
        else:
            return redirect("/Login/")
    except:
        return redirect("/Login/")


@never_cache
def update_profile(request):
    d = tbl_SignUp.objects.get(id=request.session['userid'])
    d.fullname = request.POST.get("fullname")
    d.email = request.POST.get("email")
    d.mobile = request.POST.get("mobile")
    try:
        image = request.FILES['dp']
        fs = FileSystemStorage()
        file = fs.save(image.name, image)
        url = fs.url(file)
        d.dp = url
        d.save()
    except:
        d.save()
    return redirect("/my_account/")


def remove_product(request):
    pid = request.GET.get("product_id")
    try:
        product = tbl_Cart_Products.objects.get(id=pid)

        c = tbl_Cart.objects.get(user=request.session['userid'])
        c.total = int(c.total) - int(product.total_price)
        c.sub_total = int(c.sub_total) - int(product.total_price)
        c.save()
        product.delete()
        return JsonResponse({'success': True, 'message': 'Product removed successfully'})
    except tbl_Cart_Products.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def save_password(request):
    f = tbl_SignUp.objects.get(id=request.session['userid'])
    f.password = request.POST.get("new_password")
    f.save()
    return redirect("/my_account/")


def forgot_password(request):
    return render(request, "forgot_password.html")


def password_send(request):
    email = request.POST.get("email")
    if tbl_SignUp.objects.filter(email=email).exists():
        e = tbl_SignUp.objects.get(email=email)
        password = e.password
        subject = "Password"
        Message = "Your Password is " + password
        send_mail(subject, Message, settings.EMAIL_HOST_USER, [email])
        messages.success(request, "Password sent to your email ,Please check ")
        return redirect("/forgot_password/")


@never_cache
def view_product_single_user(request, id):
    single = tbl_Product.objects.get(id=id)
    cat = tbl_Category.objects.all()
    print(single.category.id)
    interest = tbl_Product.objects.filter(category=single.category.id).exclude(id=id)
    print(interest)
    return render(request, "view_product_single.html", {"single": single, "cat": cat, "interest": interest})


def remove_from_wishlist(request, id):
    d = tbl_Wishlist.objects.get(id=id)
    d.delete()
    return redirect("/wishlist/")


def payment_success(request, id):
    inv = tbl_Checkout.objects.get(id=id)
    inv_pdt = tbl_checkout_products.objects.filter(checkout=id)
    d = date.today()
    return render(request, "payment_success.html", {"inv": inv, "inv_pdt": inv_pdt, "d": d})


def cod_invoice(request):
    order_id = generate_order_id(6)
    invoice_number = generate_invoice_number(6)

    # Check if order ID and invoice number already exist
    while order_id_exists(order_id):
        order_id = generate_order_id(6)

    while invoice_number_exists(invoice_number):
        invoice_number = generate_invoice_number(6)

    # checkout saving and stock reduce
    ca = tbl_Cart.objects.get(user=request.session['userid'])
    ca_pd = tbl_Cart_Products.objects.filter(cart=ca)
    data = tbl_Checkout()
    data.user_id = request.session['userid']
    data.item_price = request.POST.get("item_price")
    data.total_items = request.POST.get("total_items")
    data.ship_charge = request.POST.get("ship_charge")
    data.total_after_ship = request.POST.get("total_after_ship")
    data.discount = request.POST.get("discount")
    d = request.POST.get("ship")
    d1 = tbl_Shipment_Address.objects.get(id=d)
    data.ship_address_id = d1.id
    data.status = "Pending"
    data.payment_method = "COD"
    data.orderid = order_id
    data.invoice_number = invoice_number
    data.save()
    for i in ca_pd:
        data1 = tbl_checkout_products()
        data1.user_id = request.session['userid']
        data1.checkout_id = data.id
        data1.product_id = i.product.id
        data1.quantity = i.quantity
        data1.total_price = i.total_price
        data1.save()
    for j in ca_pd:
        product = j.product.id
        quantity = j.quantity
        table = tbl_Product.objects.get(id=product)
        stock = table.opening_stock - int(quantity)
        table.current_stock = stock
        table.save()

    tbl_Cart.objects.get(user=request.session['userid']).delete()
    return redirect("cod_invoice_view", id=data.id)


def cod_invoice_view(request, id):
    inv = tbl_Checkout.objects.get(id=id)
    inv_pdt = tbl_checkout_products.objects.filter(checkout=id)
    d = date.today()
    return render(request, "cod_invoice_view.html", {"inv": inv, "inv_pdt": inv_pdt, "d": d})


def pending_orders(request):
    pend = tbl_Checkout.objects.filter(status="Pending")
    return render(request, "pending_orders.html", {"pend": pend})


def out_for_delivery(request, id):
    out = tbl_Checkout.objects.get(id=id)
    del_part = tbl_Delivery_Partner.objects.all()
    return render(request, "assign_delivery_partner.html", {"out": out, "del_part": del_part})


def cancel_order(request, id):
    can = tbl_Checkout.objects.get(id=id)
    can.status = "Cancel"
    can.save()
    return redirect("/pending_orders/")


def our_for_delivery_orders(request):
    out = tbl_Checkout.objects.filter(status="Delivery")
    return render(request, "our_for_delivery_orders.html", {"out": out})


def cancelled_orders(request):
    can = tbl_Checkout.objects.filter(status="Cancel")
    return render(request, "cancelled_orders.html", {"can": can})


def view_check_products_invoice(request, id):
    inv = tbl_Checkout.objects.get(id=id)
    inv_pdt = tbl_checkout_products.objects.filter(checkout=id)
    d = date.today()
    return render(request, "view_check_products_invoice.html", {"inv": inv, "inv_pdt": inv_pdt, "d": d})

@never_cache
def completed_orders(request):
    pend = tbl_Checkout.objects.filter(status="Complete")
    return render(request, "pending_orders.html", {"pend": pend})


stripe.api_key = "sk_test_51PFfzqRvW5dEfnEOBDa78GrVV7xUTpINko6aWd9TwxdqgpVHXaeGZ3BhJcgdNmSWtaXV6Nio2ZK1CPsGW3Q4d6gm00yxWY42f9"  # Replace with your Stripe secret key


@csrf_exempt
def process_payment(request):
    print("hii")

    if request.method == 'POST':
        data = json.loads(request.body)
        # Retrieve the payment method ID from the JSON data
        payment_method_id = data.get('payment_method_id')
        print(payment_method_id)

        # Create a payment intent
        print("helloo")
        intent = stripe.PaymentIntent.create(
            amount=int(data.get("total_after_ship")) * 100,  # Amount in cents, adjust as needed
            currency='EUR',
            payment_method=payment_method_id,
            confirmation_method='manual',
            confirm=True,
            return_url='https://127.0.0.1:8000/payment_success/'
        )
        print("complete")
        ca = tbl_Cart.objects.get(user=request.session['userid'])
        ca_pd = tbl_Cart_Products.objects.filter(cart=ca)
        order_id = generate_order_id(6)
        invoice_number = generate_invoice_number(6)

        # Check if order ID and invoice number already exist
        while order_id_exists(order_id):
            order_id = generate_order_id(6)

        while invoice_number_exists(invoice_number):
            invoice_number = generate_invoice_number(6)

        ff = tbl_Checkout()
        ff.user_id = request.session['userid']
        ff.item_price = data.get("item_price")
        ff.total_items = data.get("total_items")
        ff.ship_charge = data.get("ship_charge")
        ff.total_after_ship = data.get("total_after_ship")
        ff.discount = data.get("discount")
        d = data.get("ship")
        d1 = tbl_Shipment_Address.objects.get(id=d)
        ff.ship_address_id = d1.id
        ff.status = "Pending"
        ff.payment_method = "Online"
        ff.orderid = order_id
        ff.invoice_number = invoice_number
        ff.save()
        for i in ca_pd:
            data1 = tbl_checkout_products()
            data1.user_id = request.session['userid']
            data1.checkout_id = ff.id
            data1.product_id = i.product.id
            data1.quantity = i.quantity
            data1.total_price = i.total_price
            data1.save()
        for j in ca_pd:
            product = j.product.id
            quantity = j.quantity
            table = tbl_Product.objects.get(id=product)
            stock = table.opening_stock - int(quantity)
            table.current_stock = stock
            table.best_score += 1
            table.save()

        tbl_Cart.objects.get(user=request.session['userid']).delete()
        print("hiii")
        print(ff.id, "idd")
        r = {}
        r['id'] = ff.id
        r['success'] = True
        print(r, "uuuuuuu")

        # Payment is successful, you can save the order or perform other actions here
        return JsonResponse(r)
        # except stripe.error.CardError as e:
        #     # Handle card errors
        #     print("error")
        #     return JsonResponse({'success': False, 'error': str(e)})
        # except Exception as e:
        #     # Handle other errors
        #     print("newerror")
        #     return JsonResponse({'success': False, 'error': str(e)})

    # If the request method is not POST, return a method not allowed response
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def view_check_products(request, id):
    d = tbl_checkout_products.objects.filter(checkout=id)
    return render(request, "view_check_products.html", {"d": d})


def edit_products(request, id):
    d = tbl_Product.objects.get(id=id)
    if request.method == "POST":
        d.name = request.POST.get('name')
        d.description = request.POST.get('description')
        d.price = request.POST.get('price')
        d.country_id = request.POST.get('country')
        d.brand_id = request.POST.get('brand')
        d.category_id = request.POST.get('category')
        d.opening_stock = request.POST.get('opening_stock')
        d.current_stock = request.POST.get('current_stock')
        d.product_code = request.POST.get('product_code')
        d.status = request.POST.get('status')
        d.gross_total = request.POST.get("gross_total")
        d.product_weight = request.POST.get("weight")
        d.product_measure = request.POST.get("weight_measure")
        d.tax_rate = request.POST.get("tax_rate")
        d.tax_amount = request.POST.get("tax_amount")
        try:
            image = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(image.name, image)
            url = fs.url(file)
            d.image = url
            d.save()
        except:
            d.save()
        d.save()
        return redirect("/products/")
    else:
        return render(request, "edit_products.html", {"d": d})


def delete_product(request, id):
    d = tbl_Product.objects.get(id=id)
    d.delete()
    return redirect("/products/")


def quick_enquiry(request):
    return render(request, "quick_enquiry.html")


def save_enquiry(request):
    f = tbl_Enquiry()
    f.firstname = request.POST.get("firstname")
    f.lastname = request.POST.get("lastname")
    f.email = request.POST.get("email")
    f.message = request.POST.get("message")
    f.phone = request.POST.get("phone")
    f.save()
    subject = "New Enquiry from GoMart"
    msg = f"Name: {f.firstname} {f.lastname}\nPhone: {f.phone}\nMessage: {f.message}"
    send_mail(subject, msg, f.email, [settings.EMAIL_HOST_USER])
    return redirect("/")


def filter_by_price(request):
    min_price = request.POST.get("min_price")
    max_price = request.POST.get("max_price")
    d = tbl_Product.objects.filter(price__gte=min_price, price__lte=max_price)
    cat = tbl_Category.objects.all()
    brand = tbl_Brand.objects.all()
    return render(request, "all_products.html", {"d": d, "cat": cat, "brand": brand})


def filter_by_price_category(request, id):
    min_price = request.POST.get("min_price")
    max_price = request.POST.get("max_price")
    d = tbl_Product.objects.filter(price__gte=min_price, price__lte=max_price, category=id)
    cat = tbl_Category.objects.all()
    brand = tbl_Brand.objects.all()
    c = tbl_Category.objects.get(id=id)
    return render(request, "shop_by_category.html", {"d": d, "cat": cat, "brand": brand, "c": c})


def save_assign(request):
    try:
        checkout = request.POST.get("out")
        partner = request.POST.get("name")
        print("hii")
        if tbl_Order_Assign.objects.filter(delivery=partner, pdt_checkout=checkout).exists():
            print("helloo")
            messages.error(request, "This order is already assigned to the same person.")
            return redirect("out_for_delivery", id=checkout)

        elif tbl_Order_Assign.objects.filter(pdt_checkout=checkout).exists():
            print("elif one")
            messages.error(request, "This order is already assigned.")
            return redirect("out_for_delivery", id=checkout)
        else:
            print("else")
            g = tbl_Order_Assign()
            g.delivery_id = partner
            g.pdt_checkout_id = checkout
            g.status = "new"
            g.save()
            ch = tbl_Checkout.objects.get(id=checkout)
            ch.status = "Delivery"
            ch.save()
            return redirect("/our_for_delivery_orders/")
    except:
        return redirect("/error_page/")


def error_page(request):
    return render(request, "error_page.html")


def partner_details(request):
    part = tbl_Delivery_Partner.objects.all()

    return render(request, "partner_details.html", {"part": part})


def add_new_delivery(request):
    if request.method == "POST":
        dp = tbl_Delivery_Partner()
        dp.name = request.POST.get("name")
        dp.email = request.POST.get("email")
        dp.username = request.POST.get("username")
        dp.password = request.POST.get("password")
        dp.partner_id = request.POST.get("p_id")
        img = request.FILES['image']
        fs = FileSystemStorage()
        file = fs.save(img.name, img)
        url = fs.url(file)
        dp.image = url
        dp.save()
        return redirect("/partner_details/")

    else:
        d = tbl_Delivery_Partner.objects.all().last()
        print(d)

        if d == None:
            p_id = 'GM000' + '1' + "/DP"
            print(p_id)
        else:
            d1 = d.id
            d2 = d1 + 1
            p_id = 'GM000' + str(d2) + "/DP"
            print(p_id)

    return render(request, "add_new_delivery.html", {"p_id": p_id})


def edit_partner(request, id):
    dp = tbl_Delivery_Partner.objects.get(id=id)
    if request.method == "POST":
        dp.name = request.POST.get("name")
        dp.email = request.POST.get("email")
        dp.username = request.POST.get("username")
        dp.password = request.POST.get("password")
        dp.partner_id = request.POST.get("p_id")

        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
            url = fs.url(file)
            dp.image = url
            dp.save()
        except:
            dp.save()
        return redirect("/partner_details/")
    else:
        return render(request, "edit_partner.html", {"d": dp})


def delete_partner(request, id):
    d = tbl_Delivery_Partner.objects.get(id=id)
    d.delete()
    return redirect("/partner_details/")


def log_in_off_info(request):
    logg = tbl_login_info.objects.all()
    return render(request, "log_in_off_info.html", {"logg": logg})


def GoMartDelivery(request):
    return render(request, "GoMartDelivery.html")


def login_check_delivery(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = tbl_Delivery_Partner.objects.filter(username=username, password=password)
    if user:
        us = tbl_Delivery_Partner.objects.get(username=username, password=password)
        request.session["deli"] = us.id
        logg = tbl_login_info()
        logg.username = username
        logg.password = password
        logg.save()
        return redirect("/Delivery_Home/")
    else:
        messages.error(request, "Invalid Credentials")
        return redirect("/GoMartDelivery/")


@never_cache
def Delivery_Home(request):
    try:
        ic = request.session['deli']
        return render(request, "Delivery_Home.html")
    except:
        return redirect("/GoMartDelivery/")


@never_cache
def delivery_orders(request):
    try:
        ic = request.session['deli']
        orders = tbl_Order_Assign.objects.filter(delivery=request.session["deli"], status="new")
        return render(request, "delivery_orders.html", {"orders": orders})
    except:
        return redirect("/GoMartDelivery/")


@never_cache
def delivery_orders_previous(request):
    try:
        ic = request.session['deli']
        orders = tbl_Order_Assign.objects.filter(delivery=request.session["deli"], status="complete")
        return render(request, "delivery_orders_previous.html", {"orders": orders})
    except:
        return redirect("/GoMartDelivery/")


def logout_delivery(request):
    del request.session['deli']
    return redirect("/GoMartDelivery/")


def change_password_delivery(request):
    password = tbl_Delivery_Partner.objects.get(id=request.session['deli'])
    return render(request, "change_password_delivery.html", {"password": password})


def save_change_password(request):
    new = request.POST.get("new")
    p = tbl_Delivery_Partner.objects.get(id=request.session['deli'])
    p.password = new
    p.save()
    return redirect("/Delivery_Home/")


def delivered_orders(request, id):
    d = tbl_Order_Assign.objects.get(id=id)
    d.status = "complete"
    d.save()
    f = tbl_Checkout.objects.get(id=d.pdt_checkout.id)
    f.status = "Complete"
    f.save()
    orderid = d.pdt_checkout.orderid
    total = d.pdt_checkout.total_after_ship
    email = f.user.email
    subject = "Delivery Notification"
    message = "Your Order " + str(orderid) + " is delivered successfully, Amount is " + str(total)
    message1 = (
        f"Order {orderid} is delivered successfully, Amount is {total}\n"
        f"Delivery Partner: {d.delivery.name}"
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    send_mail(subject, message1, d.delivery.email, [settings.EMAIL_HOST_USER])
    return redirect("/delivery_orders/")


def send_email_with_invoice(request):
    # Generate the invoice content (You need to implement this)

    inv = request.GET.get("inv")
    print(inv, "inv")
    inv = tbl_Checkout.objects.get(id=inv)
    inv_pdt = tbl_checkout_products.objects.filter(checkout=inv)
    d = date.today()

    # Render the invoice template to string
    html_content = render_to_string('cod_invoice_view_email.html', {'inv': inv, 'd': d, 'inv_pdt': inv_pdt})
    email_rec = inv.user.email
    # Send email
    email = EmailMessage('Invoice', html_content, settings.EMAIL_HOST_USER, [email_rec])
    email.content_subtype = 'html'  # Set the content type
    email.send()

    return JsonResponse({"status": 200})


def send_to_email_invoice(request):
    inv = request.GET.get("inv")
    print(inv, "inv")
    inv = tbl_Checkout.objects.get(id=inv)
    inv_pdt = tbl_checkout_products.objects.filter(checkout=inv)
    d = date.today()

    # Render the invoice template to string
    html_content = render_to_string('payment_success_email.html', {'inv': inv, 'd': d, 'inv_pdt': inv_pdt})
    email_rec = inv.user.email
    # Send email
    email = EmailMessage('Invoice', html_content, settings.EMAIL_HOST_USER, [email_rec])
    email.content_subtype = 'html'  # Set the content type
    email.send()

    return JsonResponse({"status": 200})


def edit_category(request, id):
    d = tbl_Category.objects.get(id=id)
    if request.method == "POST":
        d.name = request.POST.get("category")
        try:
            img = request.FILES['image']
            print()
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
            url = fs.url(file)
            d.image = url
            d.save()
        except:
            d.save()
        return redirect("/category/")
    else:
        return render(request, "edit_category.html", {"d": d})


def delete_category(request, id):
    d = tbl_Category.objects.get(id=id)
    d.delete()
    return redirect("/category/")


def edit_brands(request, id):
    d = tbl_Brand.objects.get(id=id)
    if request.method == "POST":
        d.name = request.POST.get("brands")
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
            url = fs.url(file)
            d.image = url
            d.save()
        except:
            d.save()
        return redirect("/brands/")
    else:
        return render(request, "edit_brands.html", {"d": d})


def delete_brands(request, id):
    d = tbl_Brand.objects.get(id=id)
    d.delete()
    return redirect("/brands/")


def deals(request):
    deal = tbl_Deals.objects.all()
    return render(request, "deals.html", {"deal": deal})


def add_deal(request):
    if request.method == "POST":
        de = tbl_Deals()
        de.deal_type = request.POST.get("deal_type")
        de.product_id = request.POST.get("product")
        de.deal_price = request.POST.get("deal_price")
        de.deal_end_date = request.POST.get("e_date")
        de.deal_start_date = request.POST.get("s_date")
        de.deal_end_time = request.POST.get("e_time")
        de.deal_start_time = request.POST.get("s_time")
        de.status = "Start"
        de.save()
        return redirect("/deals/")
    else:
        pdt = tbl_Product.objects.all()
        return render(request, "add_deal.html", {"pdt": pdt})


def Get_pdt_actual_price(request):
    pid = request.GET.get("pid")
    d = tbl_Product.objects.get(id=pid)
    price = d.gross_total
    data = {}
    data['message'] = price
    return JsonResponse(data)


def edit_deal(request, id):
    deal = tbl_Deals.objects.get(id=id)
    pdt = tbl_Product.objects.all()

    if request.method == "POST":
        deal.deal_type = request.POST.get("deal_type")
        deal.product_id = request.POST.get("product")
        deal.deal_price = request.POST.get("deal_price")
        deal.deal_end_date = request.POST.get("e_date")
        deal.deal_start_date = request.POST.get("s_date")
        deal.deal_end_time = request.POST.get("e_time")
        deal.deal_start_time = request.POST.get("s_time")
        deal.status = "Start"
        deal.save()
        return redirect("/deals/")
    else:
        return render(request, "edit_deal.html", {"deal": deal, "pdt": pdt})


def close_deal(request, id):
    deal = tbl_Deals.objects.get(id=id)
    deal.status = "Closed"
    deal.save()
    return redirect("/deals/")


def delete_deal(request, id):
    deal = tbl_Deals.objects.get(id=id)
    deal.delete()
    return redirect("/deals/")


def checking_deal_time(request, pid, id):
    deal = tbl_Deals.objects.get(id=id)
    current_time = datetime.now().strftime("%H:%M:%S")
    if deal.deal_start_date <= date.today() and deal.deal_end_date >= date.today():
        if deal.deal_start_time <= current_time and deal.deal_end_time >= current_time:
            return redirect("view_product_single", id=pid)
        else:
            messages.error(request, "Deal is not started")
            return redirect("/")
    else:
        messages.error(request, "Deal is not started")
        return redirect("/")


def poster1(request):
    d1=tbl_poster1.objects.get()
    d2=d1.id
    d=tbl_poster1.objects.get(id=d2)
    return render(request, "poster1.html",{"d":d})


def poster2(request):
    d1 = tbl_poster2.objects.get()
    d2 = d1.id
    d = tbl_poster2.objects.get(id=d2)
    return render(request, "poster2.html",{"d":d})


def poster3(request):
    d1 = tbl_poster3.objects.get()
    d2 = d1.id
    d = tbl_poster3.objects.get(id=d2)
    return render(request, "poster3.html",{"d":d})


def poster4(request):
    d1 = tbl_poster4.objects.get()
    d2 = d1.id
    d = tbl_poster4.objects.get(id=d2)
    return render(request, "poster4.html",{"d":d})


def poster5(request):
    d1 = tbl_poster5.objects.get()
    d2 = d1.id
    d = tbl_poster5.objects.get(id=d2)
    return render(request, "poster5.html",{"d":d})


def poster6(request):
    d1 = tbl_poster6.objects.get()
    d2 = d1.id
    d = tbl_poster6.objects.get(id=d2)
    return render(request, "poster6.html",{"d":d})


def poster7(request):
    d1 = tbl_poster7.objects.get()
    d2 = d1.id
    d = tbl_poster7.objects.get(id=d2)
    return render(request, "poster7.html",{"d":d})

def update_poster1(request,id):
    d=tbl_poster1.objects.get(id=id)
    if request.method=="POST":
        d.subtitle=request.POST.get("subtitle")
        d.heading=request.POST.get("heading")
        d.heading2=request.POST.get("heading2")
        image=request.FILES['image']
        fs=FileSystemStorage()
        file=fs.save(image.name,image)
        url=fs.url(file)
        d.image=url
        d.save()
        return redirect("/poster1/")

    else:
        return render(request,"update_poster1.html",{"d":d})


def update_poster2(request,id):
    d=tbl_poster2.objects.get(id=id)
    if request.method=="POST":
        d.subtitle=request.POST.get("subtitle")
        d.heading=request.POST.get("heading")
        d.heading2=request.POST.get("heading2")
        image=request.FILES['image']
        fs=FileSystemStorage()
        file=fs.save(image.name,image)
        url=fs.url(file)
        d.image=url
        d.save()
        return redirect("/poster2/")

    else:
        return render(request,"update_poster2.html",{"d":d})


def update_poster3(request,id):
    d=tbl_poster3.objects.get(id=id)
    if request.method=="POST":
        d.subtitle=request.POST.get("subtitle")
        d.heading=request.POST.get("heading")
        d.heading2=request.POST.get("heading2")
        image=request.FILES['image']
        fs=FileSystemStorage()
        file=fs.save(image.name,image)
        url=fs.url(file)
        d.image=url
        d.save()
        return redirect("/poster3/")

    else:
        return render(request,"update_poster3.html",{"d":d})


def update_poster4(request,id):
    d=tbl_poster4.objects.get(id=id)
    if request.method=="POST":
        d.subtitle=request.POST.get("subtitle")
        d.heading=request.POST.get("heading")
        d.heading2=request.POST.get("heading2")
        d.sentence = request.POST.get("sentence")
        image=request.FILES['image']
        fs=FileSystemStorage()
        file = fs.save(image.name, image)
        file = fs.save(image.name, image)
        url = fs.url(file)
        d.image=url
        d.save()
        return redirect("/poster4/")

    else:
        return render(request,"update_poster4.html",{"d":d})


def update_poster5(request,id):
    d=tbl_poster5.objects.get(id=id)
    if request.method=="POST":
        d.subtitle=request.POST.get("subtitle")
        d.heading=request.POST.get("heading")
        image=request.FILES['image']
        fs=FileSystemStorage()
        file=fs.save(image.name,image)
        url=fs.url(file)
        d.image=url
        d.save()
        return redirect("/poster5/")

    else:
        return render(request,"update_poster5.html",{"d":d})


def update_poster6(request,id):
    d=tbl_poster6.objects.get(id=id)
    if request.method=="POST":
        image=request.FILES['image']
        fs=FileSystemStorage()
        file=fs.save(image.name,image)
        url=fs.url(file)
        d.image=url
        d.save()
        return redirect("/poster6/")

    else:
        return render(request,"update_poster6.html",{"d":d})


def update_poster7(request,id):
    d=tbl_poster7.objects.get(id=id)
    if request.method=="POST":
        d.subtitle=request.POST.get("subtitle")
        d.title=request.POST.get("title")
        d.subtitle2=request.POST.get("subtitle2")
        image=request.FILES['image']
        fs=FileSystemStorage()
        file = fs.save(image.name, image)
        url = fs.url(file)
        d.image = url
        d.save()
        return redirect("/poster7/")

    else:
        return render(request, "update_poster7.html", {"d": d})


def add_subscription(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if tbl_Subscribe.objects.filter(email=email).exists():
            messages.error(request, "You are already subscribed")
            return redirect("/")
        else:
            data = tbl_Subscribe()
            data.email = request.POST.get("email")
            data.save()
            return redirect("/")


def My_products(request, id):
    myp = tbl_checkout_products.objects.filter(checkout=id, user=request.session['userid'])
    return render(request, "My_products.html", {"myp": myp})


def rating_products(request, id, pid):
    obj = tbl_Rating()
    obj.user_id = request.session['userid']
    obj.comment = request.POST.get("comment")
    obj.rating = request.POST.get("rating")
    obj.product_id = pid
    obj.checkout_product_id = id
    obj.status = "Rated"
    obj.save()
    return redirect("/my_account/")
