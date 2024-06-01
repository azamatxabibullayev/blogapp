from django.forms import ModelForm
from django import forms
from .models import Review, Order


class AddReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']


class UpdateReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'number']
