from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
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
        return render(request,"add_products.html",{"cou":cou,"cat":cat,"bran":bran})

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
    cat = tbl_Category.objects.all()
    coun = tbl_Country.objects.all()
    brand = tbl_Brand.objects.all()
    return render(request,"Login.html",{"cat":cat,"coun":coun,"brand":brand})


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
            password=password

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
            return redirect("/HomePage/")
        else:
            return redirect("/Login/")

def HomePage(request):
    try:
        r=request.session['userid']
        if r:
            user=tbl_SignUp.objects.get(id=r)
            return render(request,"HomePage.html",{"user":user})
        else:
            return redirect("/")
    except:
        return redirect("/")



