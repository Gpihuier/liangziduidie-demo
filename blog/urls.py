from django.urls import path
from . import views

urlpatterns = [
    # 文章详细
    path('post/<int:post_id>/view/<str:username>/', views.view_post, name='view_post'),
    # 文章阅读量统计
    path('post/<int:post_id>/stats/', views.get_post_stats, name='get_post_stats'),
]