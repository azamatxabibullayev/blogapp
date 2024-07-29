from django import forms
from .models import Category, Articles, Reviews


class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ('title', 'text', 'image')


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('comment', 'star_given')