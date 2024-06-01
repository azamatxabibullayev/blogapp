from django.db import models
from django.urls import reverse
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CategoryProducts(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'category_products'

    def __str__(self):
        return self.name


class Post(models.Model):
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, default='default_img/post_img.png')
    title = models.CharField(max_length=200)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f"Review by {self.user} for {self.post}"


class Order(models.Model):
    user = models.CharField(max_length=100)
    number = models.IntegerField()

    class Meta:
        db_table = 'order'

    def __str__(self):
        return self.number
