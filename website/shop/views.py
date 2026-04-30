from django.shortcuts import render, get_object_or_404
from .models import Category, Product, UserActivity
from django.core.paginator import Paginator

def shop(request):
    
    categories = Category.objects.filter(slug__in=['hardware', 'software'])
    return render(request, 'shop/shop.html', {'categories': categories})
    
def category(request, slug):
    
    category = get_object_or_404(Category, slug=slug)
    query = request.GET.get('q')
    products_list = Product.objects.filter(category=category, is_active=True).order_by('-id')

    if query:
        products_list = products_list.filter(name__icontains=query)

        fue_exitosa = products_list.exists()

        UserActivity.objects.create(
            user=request.user if request.user.is_authenticated else None,
            event_type='search',
            description=f"Buscó en {category.name}: {query}",
            
            ip_address=request.META.get('REMOTE_ADDR')
        )

    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.GET.get('ajax'):
        return render(request, 'layout/partials/product_list.html', {'products': page_obj})

    return render(request, 'shop/category.html', {
        'category': category,
        'products': page_obj,
        'query': query,
    })

def product_detail(request, slug):
    
    product = get_object_or_404(Product, slug=slug, is_active=True)

    UserActivity.objects.create(
        user=request.user if request.user.is_authenticated else None,
        event_type='view',
        description=f"Vio el producto: {product.name}",
        ip_address=request.META.get('REMOTE_ADDR')
    )

    return render(request, 'shop/product_detail.html', {
        'product': product, 
    })

