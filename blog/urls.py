from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:post_id>/<str:username>/', views.post_detail),
]