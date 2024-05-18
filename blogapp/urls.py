from django.urls import path
from .views import Create_post, read_post, read_blog, update_post
urlpatterns = [
    path('create', Create_post),
    path('', read_post, name='home'),
    path('post/<int:id>',read_blog),
    path('update/<int:id>', update_post, name='update')
]