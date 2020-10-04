from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from home.models import Product
from order.models import Order
from home.models import Category
# Create your views here.

class HomeView(ListView):
    model = Product
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    

class AllProductListView(ListView):
    model = Product
    template_name = "home/all_product.html"
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = "home/product-details.html"
    context_object_name = 'products'


def kitchen(request):
    try:
        orders = Order.objects.filter(ordered=True).order_by('-id')
        context ={
            'orders': orders
        }
    except:
        messages.warning(request, f"you do not have an active order")
        return redirect('home:home')
    return render(request, 'home/kitchen.html', context)
