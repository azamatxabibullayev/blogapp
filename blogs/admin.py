from django.contrib import admin
from .models import Category, Articles, UserArticleInteraction, Reviews
# Register your models here.

admin.site.register(Articles)
admin.site.register(Category)
admin.site.register(UserArticleInteraction)
admin.site.register(Reviews)