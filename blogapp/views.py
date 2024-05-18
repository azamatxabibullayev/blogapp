from django.shortcuts import render, redirect
from .models import BlogPost
# Create your views here.
def Create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('post')
        image = request.FILES.get('image')
        BlogPost.objects.create(title=title, body=body, image=image)
        return redirect('home')
    return render(request, 'create_blog_post.html')

def read_post(request):
    if request.method == 'GET':
        post = BlogPost.objects.all()
        return render(request, 'read_blog_post_home.html', {'posts': post})

def read_blog(request, id):
    if request.method == 'GET':
            post = BlogPost.objects.filter(id=id)
            return render(request, 'read_blog.html', {'posts': post})


def update_post(request, id):
    post = BlogPost.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('content')
        post.title = title
        post.body = body
        image = request.FILES.get('image')
        if image:
            post.image = image
        post.save()
        return redirect('home')
    return render(request, 'update_post.html', {'post': post})

