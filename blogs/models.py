from django.db import models
from users.models import CustomUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Articles(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    star_given = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    image = models.ImageField(upload_to='article_images/', blank=True, null=True,
                              default='default_images/not_available.png')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articles'

    def __str__(self):
        return f'{self.category.name} - {self.title}'


class UserArticleInteraction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    watch_later = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'article')


class Reviews(models.Model):
    comment = models.TextField()
    star_given = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f'{self.user} - {self.article}'
