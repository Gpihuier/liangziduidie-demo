from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from .models import Post
from .services import ReadCountService

def view_post(request, post_id, username):
    """
    获取文章内容，并记录一次阅读。
    这个视图的访问会触发阅读量增加（写操作）。
    """
    if not username:
        return JsonResponse({'error': 'Username is required.'}, status=400)

    try:
        post = get_object_or_404(Post, pk=post_id)
        service = ReadCountService(post_id=post_id)
    except ValueError as e:
        raise Http404(str(e))

    # 增加阅读量（写操作，会使缓存失效）
    service.increment_read_count(username)

    # 返回文章内容
    return JsonResponse({
        'title': post.title,
        'content': post.content,
        'message': 'success'
    })


def get_post_stats(request, post_id):
    """
    获取文章的阅读统计数据。
    """
    try:
        service = ReadCountService(post_id=post_id)
    except ValueError as e:
        raise Http404(str(e))
    
    stats = service.get_read_statistics()

    cache_hit_rate = service.get_cache_hit_rate()
    stats['cache_hit_rate'] = f"{cache_hit_rate}%"

    return JsonResponse(stats)
