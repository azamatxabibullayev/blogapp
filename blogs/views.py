from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Articles, UserArticleInteraction, Reviews
from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import ArticlesForm, ReviewsForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from users.models import CustomUser
from django.db.models import Q


# Create your views here.


class CategoryListView(View):
    def get(self, request):
        category = Category.objects.all()
        articless = Articles.objects.all()
        context = {
            'category': category,
            'articles': articless
        }
        return render(request, 'blogs/category_list.html', context=context)


class ArticlesListView(View):
    def get(self, request, pk):
        articles = Articles.objects.filter(category=pk)
        context = {
            'articles': articles,
        }
        return render(request, 'blogs/articles_list.html', context=context)


class ArticlesDetailView(View):
    def get(self, request, pk):
        article = Articles.objects.get(pk=pk)
        star_given_review = Reviews.objects.filter(article_id=pk)
        result = [review.star_given for review in star_given_review if 1 < review.star_given < 6]
        average = round(sum(result) / len(result), 1) if result else None
        return render(request, 'blogs/articles_detail.html', {'article': article, 'star_given_review':star_given_review, 'average':average})


class ArticlesUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        if article.author != request.user:
            raise PermissionDenied("You are not allowed to edit this article.")

        update_article_form = ArticlesForm(instance=article)
        context = {
            'update_article_form': update_article_form,
            'article': article
        }
        return render(request, 'blogs/articles_update.html', context=context)

    def post(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        if article.author != request.user:
            raise PermissionDenied("You are not allowed to edit this article.")

        update_article_form = ArticlesForm(request.POST, request.FILES, instance=article)
        if update_article_form.is_valid():
            update_article_form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('blogs:articles-detail', pk=article.pk)
        else:
            context = {
                'update_article_form': update_article_form,
                'article': article
            }
            return render(request, 'blogs/articles_update.html', context=context)

    def get_success_url(self):
        return reverse_lazy('blogs:articles-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Article updated successfully!")
        return response


class ArticlesCreateView(CreateView):
    model = Articles
    template_name = 'blogs/articles_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('blogs:articles-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Article added successfully!")
        return response


class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        article = Articles.objects.filter(
            Q(Q(title__icontains=query) | Q(author__username__icontains=query))
        )
        context = {
            'articles': article,
            'query': query
        }
        return render(request, 'blogs/search_results.html', context=context)


@method_decorator(login_required, name='dispatch')
class LikeArticleView(View):
    def post(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        interaction, crated = UserArticleInteraction.objects.get_or_create(user=request.user, article=article)
        interaction.liked = not interaction.liked
        messages.success(request,'Added to like')
        interaction.save()
        return redirect('blogs:articles-detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class UnlikeArticleView(View):
    def post(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        interaction = get_object_or_404(UserArticleInteraction, user=request.user, article=article)
        if interaction.liked:
            interaction.liked = False
            interaction.save()
            messages.success(request, 'Removed from Liked Articles')
        return redirect('blogs:liked-articles')

@method_decorator(login_required, name='dispatch')
class WatchLaterArticleView(View):
    def post(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        interaction, created = UserArticleInteraction.objects.get_or_create(user=request.user, article=article)
        interaction.watch_later = not interaction.watch_later
        messages.success(request, 'Added to watch later')
        interaction.save()
        return redirect('blogs:articles-detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class RemoveWatchLaterView(View):
    def post(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        interaction = get_object_or_404(UserArticleInteraction, user=request.user, article=article)
        if interaction.watch_later:
            interaction.watch_later = False
            interaction.save()
            messages.success(request, 'Removed from Watch Later')
        return redirect('blogs:watch-later-articles')


@method_decorator(login_required, name='dispatch')
class LikedArticlesView(View):
    def get(self, request):
        liked_interactions = UserArticleInteraction.objects.filter(user=request.user, liked=True)
        liked_articles = [interaction.article for interaction in liked_interactions]
        context = {
            'liked_articles': liked_articles
        }
        return render(request, 'blogs/liked_articles.html', context=context)

@method_decorator(login_required, name='dispatch')
class WatchLaterArticlesView(View):
    def get(self, request):
        interactions = UserArticleInteraction.objects.filter(user=request.user, watch_later=True)
        articles = [interaction.article for interaction in interactions]
        return render(request, 'blogs/watch_later_articles.html', {'articles': articles})


class AddReviewsView(View):
    def get(self, request, pk):
        articles = Articles.objects.get(pk=pk)
        add_review_form = ReviewsForm()
        context = {
            'articles': articles,
            'add_review_form': add_review_form
        }
        return render(request, 'blogs/add_review.html', context=context)

    def post(self, request, pk):
        articles = Articles.objects.get(pk=pk)
        add_review_form = ReviewsForm(request.POST)
        if add_review_form.is_valid():
            review = Reviews.objects.create(
                comment=add_review_form.cleaned_data['comment'],
                article=articles,
                user=request.user,
                star_given=add_review_form.cleaned_data['star_given']
            )
            review.save()
            messages.success(request, "Review added successfully.")
            return redirect('blogs:articles-detail', pk=pk)
        else:
            messages.error(request, "Failed to add review. Please check the form.")
            return render(request, 'blogs/add_review.html', {'articles': articles, 'add_review_form': add_review_form})

class ReviewsDetailView(View):
    def get(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        reviews = Reviews.objects.filter(article_id=pk)
        context = {
            'article': article,
            'reviews': reviews
        }
        return render(request, 'blogs/reviews_detail.html', context)


class ArticlesDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        if article.author != request.user:
            raise PermissionDenied("You are not allowed to delete this article.")

        context = {
            'article': article
        }
        return render(request, 'blogs/articles_delete.html', context=context)

    def post(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        if article.author != request.user:
            raise PermissionDenied("You are not allowed to delete this article.")

        article.delete()
        messages.success(request, "Article deleted successfully!")
        return redirect('blogs:articles-list', pk=pk)
