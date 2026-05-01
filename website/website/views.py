from django.shortcuts import render
from post.models import Post
from shop.models import Product
from django.http import HttpResponse

def index(request):
    
    featured_posts = Post.objects.all().order_by('-views_count', '-created_at')[:3]
    
    products = Product.objects.all().order_by('-id')[:3] 

    context = {
        'posts': featured_posts,
        'products': products 
    }
    return render(request, 'index.html', context)

def health_check(request):
    return HttpResponse("pong", content_type="text/plain")