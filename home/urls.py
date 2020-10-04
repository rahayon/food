from django.urls import path
from home import views
app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.AllProductListView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='prdocuts_detail'),
    path('kitchen/', views.kitchen, name='kitchen'),
]
