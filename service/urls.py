from django.urls import path
from service import views

app_name = 'service'

urlpatterns = [
    path('', views.Service.as_view(), name='service'),
]

