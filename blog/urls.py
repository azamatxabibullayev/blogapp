from django.urls import path
from .views import *

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit', BlogUpdateView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete', BlogDeleteView.as_view(), name='post-delete'),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('categories/', CategoryProductsListView.as_view(), name='category_products'),
    path('categories/<int:pk>/', BlogListView1.as_view(), name='posts_by_category'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('add_review/<int:pk>', AddReviewView.as_view(), name='add_review'),
    path('review_delete/<int:pk>', ReviewDeleteView.as_view(), name='review_delete'),
    path('review_update/<int:pk>', ReviewUpdateView.as_view(), name='review_update'),
]
