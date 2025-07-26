from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Post
from .services import ReadCountService

def post_detail(request, post_id, username=''):
    return JsonResponse({'post_id': post_id, 'username': username})
