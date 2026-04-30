from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product, UserActivity

@require_POST
def add_to_cart(request):
    
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')

    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError
    except (TypeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Cantidad inválida.'})

    product = get_object_or_404(Product, pk=product_id, is_active=True)

    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'image': product.image.url,
        }

    UserActivity.objects.create(
        user=request.user if request.user.is_authenticated else None,
        event_type='cart_add',
        description=f"Añadió al carrito: {product.name} (Cantidad: {quantity})",
        ip_address=request.META.get('REMOTE_ADDR')
    )

    request.session['cart'] = cart
    request.session.modified = True  

    total_items = sum(item['quantity'] for item in cart.values())

    return JsonResponse({'success': True, 'total_items': total_items})

@login_required
def cart_view(request):
    
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')

        if product_id in cart:
        
            if action == 'remove':
                del cart[product_id]
        
            elif action == 'update':
        
                try:
        
                    quantity = int(request.POST.get('quantity', 1))
        
                    if quantity > 0:
                        cart[product_id]['quantity'] = quantity
                    else:
                        del cart[product_id]
        
                except ValueError:
                    pass  

            request.session['cart'] = cart
            request.session.modified = True
            return redirect('cart:cart')

    cart_items = []
    total_price = 0
    
    for product_id, item in cart.items():
        subtotal = item['quantity'] * item['price']
        total_price += subtotal
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image': item['image'],
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    
    return render(request, 'cart/cart.html', context)

@login_required
def side_cart(request):
    
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    
    return render(request, 'layout/partials/side_cart_items.html', {
        'cart': cart,
        'total': total
    })