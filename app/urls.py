
from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index, name='index'),
    path('about', views.about, name="about"),
    path('contactus', views.contactus, name="contactus"),
    path('product', views.product, name="product"),
    path('product/filter-data',views.filter_data,name="filter-data"),
    path('product/<slug:slug>',views.product_detail, name="product_detail"),
    path('404', views.error404, name='404'),
    path('account/my-account', views.my_account, name='my_account'),
    path('account/user_register', views.user_register, name='user_register'),
    path('account/login', views.user_login, name='user_login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('account/profile', views.profile, name='profile'),
    path('account/profile/update', views.profile_update, name="profile_update"),
    
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    
    path('checkout',views.checkout, name="checkout"),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


