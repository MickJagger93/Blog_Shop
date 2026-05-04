import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import Order, OrderItem
from .forms import OrderForm, Order
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    
    if request.method == 'POST':
    
        form = OrderForm(request.POST)
    
        if form.is_valid():
    
            cart = request.session.get('cart', {})
            
            for product_id, item in cart.items():
                product = Product.objects.get(pk=product_id)
                
                if product.stock < item['quantity']:
                   
                    return render(request, 'orders/checkout.html', {
                        'form': form, 
                        'error': f'Lo sentimos, el producto {product.name} ya no tiene stock suficiente.'
                    })

            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for product_id, item in cart.items():
                product = Product.objects.get(pk=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    stock=item['quantity']
                )
            
            return redirect('orders:payment_method')
            
    else:
        form = OrderForm()
    
    return render(request, 'orders/checkout.html', {'form': form})

@login_required
def payment_method(request):
    
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart:cart')
    
    return render(request, 'orders/payment_method.html')

@login_required
def stripe_payment(request):
    
    order = Order.objects.filter(user=request.user, paid=False).last()
    
    if not order:
        return redirect('cart:cart') 

    return render(request, 'orders/stripe_payment.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'order': order 
    })

@csrf_exempt
def stripe_webhook(request):
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('client_reference_id') 
        
        if order_id:
            try:
                
                order = Order.objects.get(id=int(order_id))
                
                if not order.paid:
                    order.paid = True
                    order.save()
                    
                    for item in order.items.all():
                        product = item.product
                        product.stock -= item.stock
                        product.save()
                        
                    print(f"✅ Stock descontado para la orden {order_id}")
            
            except Order.DoesNotExist:
                print(f"❌ Orden {order_id} no encontrada")
                
    return HttpResponse(status=200)

@login_required
def create_payment(request):
    
    if request.method == 'POST':
        
        order = Order.objects.filter(user=request.user, paid=False).last()
        
        if not order:
            
            return JsonResponse({'status': 'error', 'message': 'No hay pedidos pendientes.'})

        total_compra = sum(item.price * item.stock for item in order.items.all())
        
        amount = int(total_compra * 100)
        
        token = request.POST.get('stripeToken')
        
        try:
            
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
                description=f'Pago Pedido #{order.id} - {order.full_name}',
            )
            
            order.paid = True
            order.save()

            for item in order.items.all():
                product = item.product
                product.stock -= item.stock
                product.save()

            if 'cart' in request.session:
                del request.session['cart']
            
            return JsonResponse({'status': 'success'})
            
        except stripe.error.CardError as e:
            
            return JsonResponse({'status': 'error', 'message': e.user_message})
        
        except Exception as e:
        
            return JsonResponse({'status': 'error', 'message': 'Ocurrió un error inesperado.'})
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def bank_transfer(request):
    
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart:cart')

    if request.method == 'POST':

        order = Order.objects.filter(user=request.user, paid=False).last()
        if order:
            for item in order.items.all():
                product = item.product
                product.stock -= item.stock
                product.save()

            order.paid = True
            order.save()

        request.session['cart'] = {}
        return redirect('orders:order_success')

    return render(request, 'orders/bank_transfer.html', {
        'bank_details': {
            'owner': 'xxxxxxx',
            'id_number': 'xxxxxxxx',
            'bank': 'Bank Of America',
            'account_number': '0102-XXXX-XXXX-XXXX-XXXX',
        }
    })

@login_required
def order_success(request):
    
    return render(request, 'orders/order_success.html')

@login_required
def mis_compras(request):
    
    pedidos = Order.objects.filter(user=request.user).order_by('-created_at')  
    return render(request, 'orders/mis_compras.html', {'pedidos': pedidos})

@login_required
def detalle_pedido(request, pedido_id):
    
    pedido = get_object_or_404(Order, id=pedido_id, user=request.user)
    items = pedido.items.all()
    return render(request, 'orders/detalle_pedido.html', {'pedido': pedido, 'items': items})