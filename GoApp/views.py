import json
import math
from datetime import date

import razorpay as razorpay
import requests
import stripe as stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

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
        image=request.FILES['image']
        fs=FileSystemStorage()
        file=fs.save(image.name,image)
        url=fs.url(file)
        d.image=url
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
    try:
        if request.session['userid']:
            print("hi")
            d = tbl_Product.objects.get(id=id)
            wish=tbl_Wishlist()
            wish.product_id=id
            wish.user_id=request.session['userid']
            wish.save()
            return redirect("/wishlist/")
        else:
            print("hii")

            return redirect("/Login/")
    except:
        print("hiii")
        return redirect("/Login/")

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

def cart_user(request):
    try:
        c=tbl_Cart.objects.get(user=request.session["userid"])
        cart_details=tbl_Cart_Products.objects.filter(user=request.session["userid"],cart=c)
        cat = tbl_Category.objects.all()

        return render(request,"cart_user.html",{"cart_details":cart_details,"cat":cat,"c":c})
    except:
        cat = tbl_Category.objects.all()
        return render(request,"cart_user.html",{"cat":cat})






def wishlist(request):
    wish = tbl_Wishlist.objects.filter(user=request.session["userid"])
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
                s=int(cart.sub_total)
                s+=int(price)
                cart.sub_total= s
                t=int(cart.total)
                t += int(price)
                cart.total= t
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
    table_count= tbl_Product.objects.filter(category=id).count()
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    return render(request, "shop_by_category_user.html", {"d": d, "cat": cat, "coun": coun, "brand": brand,
                                                          "table_count":table_count})

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
razorpay_client = razorpay.Client(auth=('rzp_test_sEU3RKHFgCx23a','YYzkNd8erSik7IK1tnPZL5nY'))

def checkout(request):

    ship = tbl_Shipment_Address.objects.filter(user=request.session['userid']).last()


    bill = tbl_Billing_Address.objects.filter(user=request.session['userid']).last()
    f=tbl_Cart.objects.get(user=request.session['userid'])
    total_items=tbl_Cart_Products.objects.filter(cart=f).count()

    item_price=f.sub_total
    if int(f.total) >= 50:
        ship_charge=0
        total_after_ship=f.total
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
            total_after_ship = int(f.total)+ship_charge
    currency = 'INR'
    amount = int(total_after_ship) * 100

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id

    context['razorpay_merchant_key'] = 'rzp_test_sEU3RKHFgCx23a'
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['total_items'] = total_items
    context['item_price'] = item_price
    context['ship_charge'] = ship_charge
    context['total_after_ship'] = total_after_ship
    context['d'] = ship
    context['bill'] = bill


    return render(request,"checkout.html",context)

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
    return render(request,"about.html")


def save_ship_address(request):
    data=tbl_Shipment_Address()
    data.first_name=request.POST.get("firstname")
    data.last_name=request.POST.get("lastname")
    data.email=request.POST.get("email")
    data.mobile=request.POST.get("mobile")
    data.state=request.POST.get("state")
    data.street_address=request.POST.get("street")
    data.user_id=request.session['userid']
    data.Eircode=request.POST.get("eircode")
    data.save()
    return redirect("checkout1",id=data.id)

def checkout1(request,id):
    d=tbl_Shipment_Address.objects.get(id=id)
    f = tbl_Cart.objects.get(user=request.session['userid'])
    total_items = tbl_Cart_Products.objects.filter(cart=f).count()
    item_price = f.sub_total
    if int(f.total) >= 50:
        ship_charge = 0
        total_after_ship = f.total
    else:

            eircode = d.Eircode
            # Replace with the desired Eircode
            latitude, longitude = get_location_from_eircode(eircode)
            if latitude and longitude:
                print("Latitude:", latitude)
                print("Longitude:", longitude)
            else:
                print("Location not found or error occurred")
            address = get_address_from_coordinates(latitude, longitude)
            if address:
                print("Address:", address)

            else:
                print("Address not found or error occurred")
            ship_charge = 4.95
            total_after_ship = int(f.total)+ship_charge

    currency = 'INR'
    amount = int(total_after_ship) * 100

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id

    context['razorpay_merchant_key'] = 'rzp_test_a8iORttOoYuVYF'
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['total_items'] = total_items
    context['item_price'] = item_price
    context['ship_charge'] = ship_charge
    context['total_after_ship'] = total_after_ship
    context['d'] = d

    return render(request,"checkout.html",context)
def save_bill_address(request):
    if request.method=="POST":
        data=tbl_Billing_Address()
        data.first_name=request.POST.get("firstname")
        data.last_name=request.POST.get("lastname")
        data.email=request.POST.get("email")
        data.mobile=request.POST.get("mobile")
        data.state=request.POST.get("state")
        data.street_address=request.POST.get("street")
        data.user_id=request.session['userid']
        data.Eircode=request.POST.get("eircode")
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
        return JsonResponse(data={"msg":"success"})
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
def paymenthandler(request):
    print("jiii")
    price=request.POST.get("total_after_ship")

    razorpay_order_id = request.POST.get('order_id')

    payment_id = request.POST.get('payment_id', '')
    print('paymentid:', str(payment_id))

    signature = request.POST.get('razorpay_signature', '')

    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }

    # verify the payment signature.

    print("res:")
    amount = int(price) * 100  # Rs. 200
    razorpay_client.payment.capture(payment_id, amount)

    #checkout saving and stock reduce
    ca=tbl_Cart.objects.get(user=request.session['userid'])
    ca_pd=tbl_Cart_Products.objects.filter(cart=ca)
    order_id = generate_order_id(6)
    invoice_number = generate_invoice_number(6)

    # Check if order ID and invoice number already exist
    while order_id_exists(order_id):
        order_id = generate_order_id(6)

    while invoice_number_exists(invoice_number):
        invoice_number = generate_invoice_number(6)

    data=tbl_Checkout()
    data.user_id=request.session['userid']
    data.item_price=request.POST.get("item_price")
    data.total_items=request.POST.get("total_items")
    data.ship_charge=request.POST.get("ship_charge")
    data.total_after_ship=request.POST.get("total_after_ship")
    data.discount=request.POST.get("discount")
    d = request.POST.get("ship")
    d1 = tbl_Shipment_Address.objects.get(id=d)
    data.ship_address_id = d1.id
    data.status="Pending"
    data.payment_method = "Online"
    data.orderid=order_id
    data.invoice_number=invoice_number
    data.save()
    for i in ca_pd:
        data1=tbl_checkout_products()
        data1.user_id=request.session['userid']
        data1.checkout_id=data.id
        data1.product_id=i.product.id
        data1.quantity=i.quantity
        data1.total_price=i.total_price
        data1.save()
    for j in ca_pd:
        product=j.product.id
        quantity=j.quantity
        table=tbl_Product.objects.get(id=product)
        stock=table.opening_stock - int(quantity)
        table.current_stock=stock
        table.save()


    tbl_Cart.objects.get(user=request.session['userid']).delete()
    print("hiii")
    return redirect("payment_success",id=data.id)






def all_products_user(request):
    d=tbl_Product.objects.all().order_by('-price')[:3]
    cat = tbl_Category.objects.all()
    return render(request,"all_products_user.html",{"d":d,"cat":cat})

def all_product_user_sort(request):
    d = tbl_Product.objects.all().order_by('price')[:3]
    cat = tbl_Category.objects.all()
    return render(request, "all_products_user.html", {"d": d, "cat": cat})

def my_account(request):
    try:
        if request.session['userid']:

            cat = tbl_Category.objects.all()
            my=tbl_SignUp.objects.get(id=request.session['userid'])
            ship=tbl_Shipment_Address.objects.filter(user=request.session['userid'])
            bill=tbl_Billing_Address.objects.filter(user=request.session['userid'])
            recent_orders=tbl_Checkout.objects.filter(user=request.session['userid']).order_by('-id')[:6]

            return render(request,"my_account.html",{"cat":cat,"my":my,"ship":ship,"bill":bill,
                                                     "recent_orders":recent_orders})
        else:
            return redirect("/Login/")
    except:
        return redirect("/Login/")

def update_profile(request):
    d=tbl_SignUp.objects.get(id=request.session['userid'])
    d.fullname=request.POST.get("fullname")
    d.email=request.POST.get("email")
    d.mobile=request.POST.get("mobile")
    try:
        image=request.FILES['dp']
        fs=FileSystemStorage()
        file=fs.save(image.name,image)
        url=fs.url(file)
        d.dp=url
        d.save()
    except:
        d.save()
    return redirect("/my_account/")
def remove_product(request):
    pid=request.GET.get("product_id")
    try:
        product = tbl_Cart_Products.objects.get(id=pid)
        product.delete()
        c=tbl_Cart.objects.get(user=request.session['userid'])
        c.total=int(c.total)-int(product.total_price)
        c.sub_total = int(c.sub_total) - int(product.total_price)
        c.save()
        return JsonResponse({'success': True, 'message': 'Product removed successfully'})
    except tbl_Cart_Products.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def save_password(request):
    f=tbl_SignUp.objects.get(id=request.session['userid'])
    f.password=request.POST.get("new_password")
    f.save()
    return redirect("/my_account/")

def forgot_password(request):
    return render(request,"forgot_password.html")


def password_send(request):
    email=request.POST.get("email")
    if tbl_SignUp.objects.filter(email=email).exists():
        e=tbl_SignUp.objects.get(email=email)
        password=e.password
        subject="Password"
        Message="Your Password is "+password
        send_mail(subject,Message,settings.EMAIL_HOST_USER,[email])
        messages.success(request,"Password sent to your email ,Please check ")
        return redirect("/forgot_password/")


def view_product_single_user(request,id):
    single=tbl_Product.objects.get(id=id)
    return render(request,"view_product_single_user.html",{"single":single})

def remove_from_wishlist(request,id):
    d=tbl_Wishlist.objects.get(id=id)
    d.delete()
    return redirect("/wishlist/")


def payment_success(request,id):
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

    #checkout saving and stock reduce
    ca=tbl_Cart.objects.get(user=request.session['userid'])
    ca_pd=tbl_Cart_Products.objects.filter(cart=ca)
    data=tbl_Checkout()
    data.user_id=request.session['userid']
    data.item_price=request.POST.get("item_price")
    data.total_items=request.POST.get("total_items")
    data.ship_charge=request.POST.get("ship_charge")
    data.total_after_ship=request.POST.get("total_after_ship")
    data.discount=request.POST.get("discount")
    d=request.POST.get("ship")
    d1 = tbl_Shipment_Address.objects.get(id=d)
    data.ship_address_id=d1.id
    data.status="Pending"
    data.payment_method="COD"
    data.orderid=order_id
    data.invoice_number=invoice_number
    data.save()
    for i in ca_pd:
        data1=tbl_checkout_products()
        data1.user_id=request.session['userid']
        data1.checkout_id=data.id
        data1.product_id=i.product.id
        data1.quantity=i.quantity
        data1.total_price=i.total_price
        data1.save()
    for j in ca_pd:
        product=j.product.id
        quantity=j.quantity
        table=tbl_Product.objects.get(id=product)
        stock=table.opening_stock - int(quantity)
        table.current_stock=stock
        table.save()


    tbl_Cart.objects.get(user=request.session['userid']).delete()
    return redirect("cod_invoice_view",id=data.id)

def cod_invoice_view(request,id):
    inv=tbl_Checkout.objects.get(id=id)
    inv_pdt=tbl_checkout_products.objects.filter(checkout=id)
    d=date.today()
    return render(request,"cod_invoice_view.html",{"inv":inv,"inv_pdt":inv_pdt,"d":d})

def pending_orders(request):
    pend=tbl_Checkout.objects.filter(status="Pending")
    return render(request,"pending_orders.html",{"pend":pend})

def view_check_products_invoice(request,id):
    inv = tbl_Checkout.objects.get(id=id)
    inv_pdt = tbl_checkout_products.objects.filter(checkout=id)
    d = date.today()
    return render(request, "view_check_products_invoice.html", {"inv": inv, "inv_pdt": inv_pdt, "d": d})

def completed_orders(request):
    pend = tbl_Checkout.objects.filter(status="Complete")
    return render(request, "pending_orders.html", {"pend": pend})
stripe.api_key = "sk_test_51P6RmX022XTem7DHqwFRVz2gu5TTcapnV2FPnNg8vIaaLl1NT5olr5QQNxcGXB7zztaPMcC1DkxXEjqmYhVOt1nm004SicdbKv"  # Replace with your Stripe secret key

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
                amount=int(data.get("total_after_ship"))*100,  # Amount in cents, adjust as needed
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
                table.save()

            tbl_Cart.objects.get(user=request.session['userid']).delete()
            print("hiii")
            print(ff.id,"idd")
            r={}
            r['id']=ff.id
            r['success']=True
            print(r,"uuuuuuu")


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

def view_check_products(request,id):
    d=tbl_checkout_products.objects.filter(checkout=id)
    return render(request,"view_check_products.html",{"d":d})