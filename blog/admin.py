from django.contrib import admin
from .models import Post, Review, CategoryProducts

# Register your models here.

admin.site.register(CategoryProducts)
admin.site.register(Review)
admin.site.register(Post)
