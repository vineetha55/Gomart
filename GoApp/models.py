from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class tbl_Country(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class tbl_Tax(models.Model):
    country = models.ForeignKey(tbl_Country, on_delete=models.CASCADE, null=True)
    rate = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class tbl_Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class tbl_Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to="media", null=True)

    def __str__(self):
        return self.name


class tbl_Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    price = models.FloatField(null=True)
    country = models.ForeignKey(tbl_Country, on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey(tbl_Brand, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(tbl_Category, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=100, default='Active', null=True)
    opening_stock = models.PositiveIntegerField(default=0, null=True)
    current_stock = models.PositiveIntegerField(default=0, null=True)
    product_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    tax_rate = models.CharField(max_length=100, null=True)
    tax_amount = models.FloatField(null=True)
    product_weight = models.CharField(max_length=100, null=True)
    product_measure = models.CharField(max_length=100, null=True)
    gross_total = models.FloatField(null=True)
    best_score = models.IntegerField(null=True, default=1)

    def __str__(self):
        return self.name if self.name else 'Unnamed Product'


class tbl_SignUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=20, null=True)
    fullname = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    dp = models.ImageField(upload_to="media", null=True)

    def __str__(self):
        return self.email


class tbl_Wishlist(models.Model):
    user = models.ForeignKey(tbl_SignUp, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(tbl_Product, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class tbl_Cart(models.Model):
    user = models.ForeignKey(tbl_SignUp, on_delete=models.CASCADE, null=True)
    sub_total = models.FloatField(null=True)
    total = models.FloatField(null=True)


class tbl_Cart_Products(models.Model):
    cart = models.ForeignKey(tbl_Cart, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(tbl_SignUp, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(tbl_Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    total_price = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class tbl_Shipment_Address(models.Model):
    user = models.ForeignKey(tbl_SignUp, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    state = models.CharField(max_length=100)
    Eircode = models.CharField(max_length=20)


class tbl_Billing_Address(models.Model):
    user = models.ForeignKey(tbl_SignUp, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    state = models.CharField(max_length=100)
    Eircode = models.CharField(max_length=20)


class tbl_Checkout(models.Model):
    user = models.ForeignKey(tbl_SignUp, on_delete=models.CASCADE, null=True)
    orderid = models.IntegerField(null=True)
    invoice_number = models.IntegerField(null=True)
    total_items = models.CharField(max_length=100, null=True)
    item_price = models.FloatField(null=True)
    ship_charge = models.FloatField(null=True)
    total_after_ship = models.FloatField(null=True)
    discount = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ship_address = models.ForeignKey(tbl_Shipment_Address, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=100, null=True)
    payment_method = models.CharField(max_length=100, null=True)


class tbl_checkout_products(models.Model):
    checkout = models.ForeignKey(tbl_Checkout, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(tbl_SignUp, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(tbl_Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    total_price = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class tbl_Enquiry(models.Model):
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    message = models.TextField(null=True)


class tbl_Delivery_Partner(models.Model):
    partner_id = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="media", null=True)
    email = models.EmailField(null=True)
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class tbl_login_info(models.Model):
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    login_at_date = models.DateField(auto_now_add=True)
    login_at_time = models.TimeField(auto_now_add=True)

class tbl_Order_Assign(models.Model):
    delivery = models.ForeignKey(tbl_Delivery_Partner, on_delete=models.CASCADE, null=True)
    pdt_checkout = models.ForeignKey(tbl_Checkout, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, null=True)
