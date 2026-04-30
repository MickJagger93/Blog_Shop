from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.shortcuts import render
from post.models import Post
from shop.models import Product

def index(request):
    featured_posts = Post.objects.all().order_by('-views_count', '-created_at')[:3]
    
    # Traemos los productos directamente, sin filtros de ventas por ahora
    products = Product.objects.all().order_by('-id')[:3] 

    context = {
        'posts': featured_posts,
        'products': products 
    }
    return render(request, 'index.html', context)