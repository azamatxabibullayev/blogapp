from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
# Create your models here.


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='users_images/', blank=True, null=True, default='default_images/user_image.png')
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    class Meta:
        db_table = 'customuser'

    def __str__(self):
        return f'{self.username}'
