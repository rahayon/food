from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('sign_up/', views.signup, name='sign_up'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change_profile/', views.change_profile, name='change_profile'),
]
