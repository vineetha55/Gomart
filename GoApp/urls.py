from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path("Gomart_Admin/",views.Admin_login),
    path("login/check/",views.login_check),
    path("Admin_Home/",views.Admin_Home),
    path("country/",views.country),
    path("add_country/",views.add_country),
    path("brands/",views.brands),
    path("add_brands/",views.add_brands),
    path("category/",views.category),
    path("add_category/",views.add_category),
    path("products/",views.products),
    path("add_product/",views.add_product),
    path("show_by_country/<id>",views.show_by_country),
    path("show_by_brand/<id>",views.show_by_brand),
    path("shop_by_category/<id>",views.shop_by_category),
    path("logout_admin/",views.logout_admin),
    path("contact/",views.contact),
    path("Login/",views.Login,name="Login"),
    path("save_signup/",views.save_signup),
    path("check_email/",views.check_email),
    path("check_login/",views.check_login,name="check_login"),
    path("HomePage/",views.HomePage,name="HomePage"),
    path("add_to_wishlist/<id>",views.add_to_wishlist,name="add_to_wishlist"),
    path("add_vat_gst/",views.add_vat_gst,name="add_vat_gst"),
    path("view_product_single/<id>",views.view_product_single,name="view_product_single"),

    path("cart_user/",views.cart_user,name="cart_user"),

    path("wishlist/",views.wishlist,name="wishlist"),
    path("all_products/",views.all_products,name="all_products"),
    path("add_to_cart_products/<id>/<price>",views.add_to_cart_products,name="add_to_cart_products"),
    path("signup/",views.signup,name="signup"),
    path("shop_by_category_user/<id>",views.shop_by_category_user,name="shop_by_category_user"),
    path("signout_user/",views.signout_user,name="signout_user"),
    path("update_cart_products/",views.update_cart_products,name="update_cart_products"),
    path("update_cart_total/",views.update_cart_total,name="update_cart_total"),
    path("checkout/",views.checkout,name="checkout"),
    path("about/",views.about,name="about"),
    path("save_ship_address/",views.save_ship_address,name="save_ship_address"),
    path("save_bill_address/",views.save_bill_address,name="save_bill_address"),
    path("checkout1/<id>",views.checkout1,name="checkout1"),

    path("paymenthandler/",views.paymenthandler,name="paymenthandler"),
    path("all_products_user/",views.all_products_user,name="all_products_user"),
    path("my_account/",views.my_account,name="my_account"),
    path("remove_product/",views.remove_product,name="remove_product")


]
