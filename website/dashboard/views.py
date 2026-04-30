import json
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from shop.models import UserActivity, Product
from django.utils import timezone
from datetime import timedelta  
from django.contrib import messages
from orders.models import OrderItem
from django.http import JsonResponse

@staff_member_required
def dashboard(request):
    
    periodo = request.GET.get('periodo', 'todo') 
    ahora = timezone.now()
    
    actividades = UserActivity.objects.all()
    pedidos_items = OrderItem.objects.all()

    if periodo == 'hoy':
        
        filtro_date = Q(created_at__date=ahora.date())
        actividades = actividades.filter(filtro_date)
        pedidos_items = pedidos_items.filter(order__created_at__date=ahora.date())
    
    elif periodo == 'semana':
        
        hace_7 = ahora - timedelta(days=7)
        actividades = actividades.filter(created_at__gte=hace_7)
        pedidos_items = pedidos_items.filter(order__created_at__gte=hace_7)
    
    elif periodo == 'mes':
        
        hace_30 = ahora - timedelta(days=30)
        actividades = actividades.filter(created_at__gte=hace_30)
        pedidos_items = pedidos_items.filter(order__created_at__gte=hace_30)

    productos_con_actividad = Product.objects.all()[:10] 
    
    search_labels = []
    data_buscados = []
    data_vendidos = []
    data_carrito = []

    for prod in productos_con_actividad:
        search_labels.append(prod.name)
        
        buscados = actividades.filter(event_type='search', description__icontains=prod.name).count()
        data_buscados.append(buscados)
        
        vendidos = pedidos_items.filter(product=prod, order__paid=True).aggregate(total=Sum('stock'))['total'] or 0
        data_vendidos.append(vendidos)
        
        carrito = pedidos_items.filter(product=prod, order__paid=False).aggregate(total=Sum('stock'))['total'] or 0
        data_carrito.append(carrito)

    top_searches = actividades.filter(event_type='search') \
        .values('description') \
        .annotate(total=Count('description')) \
        .order_by('-total')[:5]

    top_posts = actividades.filter(event_type='post_view') \
        .values('description') \
        .annotate(total=Count('description')) \
        .order_by('-total')[:5]

    busquedas_tabla = actividades.filter(event_type='search') \
        .values('description') \
        .annotate(total=Count('description')) \
        .order_by('-total')[:10]

    context = {
        'periodo': periodo,
        'search_labels': [i['description'].replace('Buscó: ', '') for i in top_searches],
        'search_data': [i['total'] for i in top_searches],
        
        'vendidos_data': [5, 10, 2, 8, 4], 
        'carrito_data': [2, 3, 1, 5, 2],  
        
        'post_labels': [i['description'].replace('Leyó el post: ', '') for i in top_posts],
        'post_data': [i['total'] for i in top_posts],
        'busquedas_tabla': busquedas_tabla,
    }

    return render(request, 'dashboard/dashboard.html', context)

@staff_member_required
def clean_history(request):
    
    if request.method == 'POST':
        UserActivity.objects.all().delete()
        messages.success(request, "El historial de actividad ha sido borrado correctamente.")
    return redirect('dashboard:dashboard') 

@staff_member_required
def register_clic(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre_producto = data.get('producto')
            
            if nombre_producto:
                
                UserActivity.objects.create(
                    event_type='search', 
                    description=f"Buscó: {nombre_producto}"
                )
                return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'invalid method'}, status=405)