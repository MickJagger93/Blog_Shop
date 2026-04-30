from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import Post
from shop.models import UserActivity

def post(request):
    
    all_posts = Post.objects.order_by('-created_at')
    paginator = Paginator(all_posts, 9)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
    }

    return render(request, 'post/post.html', context)

@csrf_protect 
def hit_view(request, pk):
    
    if request.method == 'POST':
    
        post = get_object_or_404(Post, pk=pk)
        post.views_count += 1
        post.save()

        UserActivity.objects.create(
            user=request.user if request.user.is_authenticated else None,
            event_type='post_view',
            description=f"Leyó el post: {post.title}",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)