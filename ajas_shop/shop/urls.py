from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('cart',views.cart_page,name='cart'),
    path('fav',views.fav_page,name='fav'),
    path('favviewpage',views.favviewpage,name='favviewpage'),
    path('oder_s',views.oder_s,name='oder_s'),
    path('buy_now',views.buy_now,name='buy_now'),
    path('remove_cart/<str:cid>',views.remove_cart,name='remove_cart'),
    path('remove_fav/<str:fid>',views.remove_fav,name='remove_fav'),
    path('register',views.register,name='register'),
    path('collection',views.collection,name='collection'),
    path('collection/<str:name>',views.collectionviews,name='collection'),
    path('collection/<str:cname>/<str:pname>',views.product_detials,name='product_detials'),
    path('addtocart',views.add_to_cart,name='addtocart'),
]