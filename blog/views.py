from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post, CategoryProducts, Review, Order
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import AddReviewForm, UpdateReviewForm


# Create your views here.

class CategoryProductsListView(View):
    def get(self, request):
        categories = CategoryProducts.objects.all()
        return render(request, 'category_products.html', {'categories': categories})


class BlogListView1(ListView):
    model = Post
    template_name = 'post_list.html'


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body']


class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post-edit.html'
    fields = ['title', 'body']


class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


class AddReviewView(View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.post = post
            review.user = request.user  # request.user should be an instance of CustomUser
            review.save()
            return redirect('post_detail', pk=post.pk)
        else:
            return render(request, 'post_detail.html', {'form': form, 'post': post})


class ReviewDeleteView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post_pk = post.pk
        post.delete()
        messages.success(request, "Your comment deleted successfully!")
        return redirect('post_detail', pk=post_pk)


class ReviewUpdateView(View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        update_form = UpdateReviewForm(instance=review)
        return render(request, 'update_review.html', {'form': update_form})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        update_form = UpdateReviewForm(request.POST, instance=review)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Your comment updated successfully!")
            return redirect('post_detail', pk=review.clothe.pk)
        else:
            messages.error(request, "Failed to update your comment.")
            return render(request, 'update_review.html', {'form': update_form})


class SearchResultsView(View):
    template_name = 'home.html'

    def get(self, request):
        query = request.GET.get('q')
        posts = Post.objects.filter(name__icontains=query)
        return render(request, self.template_name, {'posts': posts})

