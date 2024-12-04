from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('post/', views.post_page, name='post'),
    path("", views.homepage, name="homepage")
]