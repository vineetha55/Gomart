from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.sample),
    path("index/", views.index),
    path("Gomart_Admin/", views.Admin_login,name="Gomart_Admin"),
    path("login/check/", views.login_check),
    path("Admin_Home/", views.Admin_Home),
    path("country/", views.country),
    path("add_country/", views.add_country),
    path("brands/", views.brands),
    path("add_brands/", views.add_brands),
    path("category/", views.category),
    path("add_category/", views.add_category),
    path("products/", views.products),
    path("add_product/", views.add_product),
    path("show_by_country/<id>", views.show_by_country),
    path("show_by_brand/<id>", views.show_by_brand),
    path("shop_by_category/<id>", views.shop_by_category),
    path("logout_admin/", views.logout_admin),
    path("contact/", views.contact),
    path("Login/", views.Login, name="Login"),
    path("save_signup/", views.save_signup),
    path("check_email/", views.check_email),
    path("check_login/", views.check_login, name="check_login"),
    path("HomePage/", views.HomePage, name="HomePage"),
    path("add_to_wishlist/<id>", views.add_to_wishlist, name="add_to_wishlist"),
    path("add_vat_gst/", views.add_vat_gst, name="add_vat_gst"),
    path("view_product_single/<id>", views.view_product_single, name="view_product_single"),

    path("cart_user/", views.cart_user, name="cart_user"),

    path("wishlist/", views.wishlist, name="wishlist"),
    path("all_products/", views.all_products, name="all_products"),
    # path("add_to_cart_products/<id>/<price>", views.add_to_cart_products, name="add_to_cart_products"),
    path("add_to_cart_products/", views.add_to_cart_products, name="add_to_cart_products"),
    path("signup/", views.signup, name="signup"),
    path("shop_by_category_user/<id>", views.shop_by_category_user, name="shop_by_category_user"),
    path("signout_user/", views.signout_user, name="signout_user"),
    path("update_cart_products/", views.update_cart_products, name="update_cart_products"),
    path("update_cart_total/", views.update_cart_total, name="update_cart_total"),
    path("checkout/", views.checkout, name="checkout"),
    path("about/", views.about, name="about"),
    path("save_ship_address/", views.save_ship_address, name="save_ship_address"),
    path("save_bill_address/", views.save_bill_address, name="save_bill_address"),
    path("checkout1/<id>", views.checkout1, name="checkout1"),

    # path("paymenthandler/",views.paymenthandler,name="paymenthandler"),
    path("all_products_user/", views.all_products_user, name="all_products_user"),
    path("my_account/", views.my_account, name="my_account"),
    path("remove_product/", views.remove_product, name="remove_product"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("password_send/", views.password_send, name="password_send"),
    path("view_product_single_user/<id>", views.view_product_single_user, name="view_product_single_user"),
    path("remove_from_wishlist/<id>", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("payment_success/<id>", views.payment_success, name="payment_success"),
    path("cod_invoice/", views.cod_invoice, name="cod_invoice"),
    path("cod_invoice_view/<id>", views.cod_invoice_view, name="cod_invoice_view"),
    path("pending_orders/", views.pending_orders, name="pending_orders"),
    path("view_check_products_invoice/<id>", views.view_check_products_invoice, name="view_check_products_invoice"),
    path("completed_orders/", views.completed_orders, name="completed_orders"),

    path("process_payment/", views.process_payment, name="process_payment"),
    path("view_check_products/<id>", views.view_check_products, name="view_check_products"),
    path("all_product_user_sort/", views.all_product_user_sort, name="all_product_user_sort"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("save_password/", views.save_password, name="save_password"),
    path("edit_products/<id>", views.edit_products, name="edit_products"),
    path("quick-enquiry/", views.quick_enquiry, name="quick_enquiry"),
    path("save_enquiry/", views.save_enquiry, name="save_enquiry"),
    path("filter_by_price/", views.filter_by_price, name="filter_by_price"),
    path("add_to_cart_products_single/<id>/<price>/<q>", views.add_to_cart_products_single,
         name="add_to_cart_products_single"),
path("add_to_cart_products_single1/<id>/<price>/<q>", views.add_to_cart_products_single1,
         name="add_to_cart_products_single1"),
    path("all_products_sort/", views.all_products_sort, name="all_products_sort"),
    path("filter_by_price_category/<id>", views.filter_by_price_category, name="filter_by_price_category"),
    path("shop_by_category_sort/<id>", views.shop_by_category_sort, name="shop_by_category_sort"),

    path("shop_by_category_user_sort/<id>", views.shop_by_category_user_sort, name="shop_by_category_user_sort"),

    path("out_for_delivery/<id>", views.out_for_delivery, name="out_for_delivery"),
    path("cancel_order/<id>", views.cancel_order, name="cancel_order"),
    path("cancelled_orders/", views.cancelled_orders, name="cancelled_orders"),
    path("our_for_delivery_orders/", views.our_for_delivery_orders, name="our_for_delivery_orders"),
    path("save_assign/", views.save_assign, name="save_assign"),
    path("error_page/", views.error_page, name="error_page"),
    path("partner_details/", views.partner_details, name="partner_details"),
    path("add_new_delivery/", views.add_new_delivery, name="add_new_delivery"),
    path("edit_partner/<id>", views.edit_partner, name="edit_partner"),
    path("delete_partner/<id>", views.delete_partner, name="delete_partner"),
    path("log_in_off_info/", views.log_in_off_info, name="log_in_off_info"),
    path("GoMartDelivery/", views.GoMartDelivery, name="GoMartDelivery"),
    path("login/check/delivery/", views.login_check_delivery, name="login_check_delivery"),
    path("Delivery_Home/", views.Delivery_Home, name="Delivery_Home"),
    path("delivery_orders/", views.delivery_orders, name="delivery_orders"),
    path("delivery_orders_previous/", views.delivery_orders_previous, name="delivery_orders_previous"),
    path("logout_delivery/", views.logout_delivery, name="logout_delivery"),
    path("change_password_delivery/", views.change_password_delivery, name="change_password_delivery"),
    path("save_change_password/", views.save_change_password, name="save_change_password"),
    path("delivered_orders/<id>", views.delivered_orders, name="delivered_orders"),
    path("send_email_with_invoice/", views.send_email_with_invoice, name="send_email_with_invoice"),
    path("send_to_email_invoice/", views.send_to_email_invoice, name="send_to_email_invoice"),
    path("edit_category/<id>", views.edit_category, name="edit_category"),
    path("delete_category/<id>", views.delete_category, name="delete_category"),
    path("edit_brands/<id>", views.edit_brands, name="edit_brands"),
    path("delete_brands/<id>", views.delete_brands, name="delete_brands"),
    path("delete_product/<id>", views.delete_product, name="delete_product"),
    path("deals/",views.deals,name="deals"),
    path("add_deal/",views.add_deal,name="add_deal"),
    path("Get_pdt_actual_price/",views.Get_pdt_actual_price,name="Get_pdt_actual_price"),
    path("edit_deal/<id>",views.edit_deal,name="edit_deal"),
    path("delete_deal/<id>",views.delete_deal,name="delete_deal"),
    path("close_deal/<id>",views.close_deal,name="close_deal"),
    path("checking_deal_time/",views.checking_deal_time,name="checking_deal_time"),
    path("checking_deal_time_user/",views.checking_deal_time_user,name="checking_deal_time_user"),
    path("poster1/",views.poster1,name="poster1"),
    path("poster2/",views.poster2,name="poster2"),
    path("poster3/", views.poster3, name="poster3"),
    path("poster4/", views.poster4, name="poster4"),
    path("poster5/", views.poster5, name="poster5"),
    path("poster6/", views.poster6, name="poster6"),
    path("poster7/", views.poster7, name="poster7"),
    path("update_poster1/<id>",views.update_poster1,name="update_poster1"),
    path("update_poster2/<id>", views.update_poster2, name="update_poster2"),
    path("update_poster3/<id>", views.update_poster3, name="update_poster3"),
    path("update_poster4/<id>", views.update_poster4, name="update_poster4"),
    path("update_poster5/<id>", views.update_poster5, name="update_poster5"),
    path("update_poster6/<id>", views.update_poster6, name="update_poster6"),
    path("update_poster7/<id>", views.update_poster7, name="update_poster7"),
    path("add-subscription/", views.add_subscription, name="add_subscription"),
    path("My-products/<id>",views.My_products,name="My_products"),
    path("rating-products/<id>/<pid>",views.rating_products,name="rating_products"),
    path("edit_country/<id>",views.edit_country,name="edit_country"),
    path("delete_country/<id>",views.delete_country,name="delete_country"),
    path("change_password_owner/",views.change_password_owner,name="change_password_owner"),
    path("update_password/",views.update_password,name="update_password"),
    path("admin_product_feedback/",views.admin_product_feedback,name="admin_product_feedback"),
    path("delete_product_feedback/<id>",views.delete_product_feedback,name="delete_product_feedback"),
    path("admin_site_feedback/",views.admin_site_feedback,name="admin_site_feedback"),
    path("confirm_feedback/<id>",views.confirm_feedback,name="confirm_feedback"),
    path("all_enquiries/",views.all_enquiries,name="all_enquiries"),
    path("delete_enquiry/<id>",views.delete_enquiry,name="delete_enquiry"),
    path("all_subscription/",views.all_subscription,name="all_subscription"),
    path("delete_subscription/<id>",views.delete_subscription,name="delete_subscription"),
    path("all_customers/",views.all_customers,name="all_customers"),
    path("block_customer/<id>",views.block_customer,name="block_customer"),
    path("email_to_subscribers/",views.email_to_subscribers,name="email_to_subscribers"),
    path("send_email_sub/",views.send_email_sub,name="send_email_sub"),
    path("view_product_single1/<id>/<deal>",views.view_product_single1,name="view_product_single1"),
    path("edit_shipping_address/<id>",views.edit_shipping_address,name="edit_shipping_address"),
    path("edit_billing_address/<id>",views.edit_billing_address,name="edit_billing_address"),
    path("all_products_high/",views.all_products_high,name="all_products_high"),
    path("wishlist_to_cart/<id>/<price>/<wid>",views.wishlist_to_cart,name="wishlist_to_cart"),
    path("all_products_high_user/",views.all_products_high_user,name="all_products_high_user"),
    path("shop_by_category_high_user/<id>",views.shop_by_category_high_user,name="shop_by_category_high_user"),
    path("shop_by_category_high/<id>",views.shop_by_category_high,name="shop_by_category_high"),
    path("search-results/",views.search_results,name="search-results"),
    path("delete-cart-all/",views.delete_cart_all,name="delete-cart-all"),
    path("delete-selected-item/",views.delete_selected_item,name="delete-selected-item"),
    path("download_database/",views.download_database,name="download_database")
]
