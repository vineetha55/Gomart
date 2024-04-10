import math

import razorpay as razorpay
import requests
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
razorpay_client = razorpay.Client(auth=('rzp_test_a8iORttOoYuVYF', 'jTA4P5JVxitd8d4bGerNCFyp'))

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
        if ship:
            eircode=ship.Eircode
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
        else:
            ship_charge = 0
            total_after_ship = f.total
    currency = 'EUR'
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

    currency = 'EUR'
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

def paymenthandler(request):
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
    data=tbl_Checkout()
    data.user_id=request.session['userid']
    data.item_price=request.POST.get("item_price")
    data.total_items=request.POST.get("total_items")
    data.ship_charge=request.POST.get("ship_charge")
    data.total_after_ship=request.POST.get("total_after_ship")
    data.discount=request.POST.get("discount")
    data.save()
    for i in ca_pd:
        data1=tbl_checkout_products()
        data1.user_id=request.session['userid']
        data1.checkout_id=data.id
        data1.product_id=i.product.id
        data1.quantity=i.quantity
        data1.total=i.total
        data1.sub_total=i.sub_total
        data1.save()
    for j in ca_pd:
        product=j.product.id
        quantity=j.quantity
        table=tbl_Product.objects.get(id=product)
        stock=table.opening_stock - int(quantity)
        table.current_stock=stock
        table.save()


    tbl_Cart.objects.get(user=request.session['userid']).delete()

    return redirect("/payment_success/")






def all_products_user(request):
    d=tbl_Product.objects.all()
    cat = tbl_Category.objects.all()
    return render(request,"all_products_user.html",{"d":d,"cat":cat})


def my_account(request):
    return render(request,"my_account.html")


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
