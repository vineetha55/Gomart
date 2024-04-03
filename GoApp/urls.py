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
    path("Login/",views.Login),
    path("save_signup/",views.save_signup),
    path("check_email/",views.check_email),
    path("check_login/",views.check_login,name="check_login"),
    path("HomePage/",views.HomePage,name="HomePage"),
    path("add_to_wishlist/<id>",views.add_to_wishlist,name="add_to_wishlist"),
    path("add_vat_gst/",views.add_vat_gst,name="add_vat_gst")
]
