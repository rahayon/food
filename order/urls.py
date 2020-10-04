from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('add/<pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<pk>/', views.remove_from_cart, name='remove'),
    path('increase/<pk>/', views.increase_cart, name='increase_cart'),
    path('decrease/<pk>/', views.decrease_cart, name='decrease_cart'),
]
