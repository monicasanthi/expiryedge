from django.urls import path
from .import views
urlpatterns=[
    path('',views.index),
    path('welcome/',views.welcome),
    path('about/',views.about),
    path('user_signup/', views.signup),
    path('user_signin/', views.user_login),
    path('o_d/',views.owner_dashboard),
    path('pro_s/',views.product_summary),
    path('expired_pro/',views.expired_product),
    path('s_d/',views.staff_dashboard),
    path('p_d/',views.product_details),
    path('p_list/',views.product_list),
    path('billing/',views.billing),
    path('save_billing/', views.save_billing, name='save_billing'),
    path('stock_m/',views.stock_maintenance),
    path('r_s/',views.restock_products),

    path('settings/',views.settings),
    path('u_profile/',views.update_profile),
    path('c_pass/',views.change_password),
    path('faq/',views.faq),
    path('r_issue/',views.report_issue),
    path('t_o_s/',views.terms_of_service),

    # path("", views.scanner_page, name="scanner_page"),  # Render the HTML page
    path("scan/", views.barcode_scanner, name="barcode_scanner"),  # API for scanning
    
    



]