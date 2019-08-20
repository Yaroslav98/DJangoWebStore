
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .import views
urlpatterns = [
    path('', views.home,name="home"),
    path('about/',views.about_view,name='about'),
    path('faq/', views.faq_view, name='faq'),
    path('categories/', views.category_view,name='categories'),
    path('product/<int:product_id>/', views.product_view,name='product'),
    path('brand/<int:brand_id>/', views.brand_view,name='brand'),
    path('products/',views.products,name='product_search'),
    path('brands/',views.brands_view,name='brands'),
    path('brand/<int:brand_id>/products/', views.brand_products_view,name='brand_product_search'),
    path('category/<int:category_id>/products/', views.category_products_view,name='category_product_search'),
    path('registration/', views.registration_view,name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account_info/', views.account_info_view, name='account_info'),
    path('account_info_edit/', views.account_info_edit_view, name='account_info_edit'),
    path('account_orders/', views.account_orders_view, name='account_orders'),
    path('order_info/<int:order_id>', views.order_info_view, name='order_info'),
    path('add_to_cart/',views.add_product_in_cart,name='add_to_cart'),
    path('remove_from_cart/',csrf_exempt(views.remove_from_cart),name='remove_from_cart'),
    path('creating_order/',views.creating_order,name='creating_order'),
    path('dynamic_search/',views.dynamic_search,name='dynamic_search'),
    path('product/<int:product_id>/creating_review/',views.creating_review,name='creating_review'),
    path('product/<int:product_id>/product_reviews/',views.product_reviews,name='product_reviews'),

]
