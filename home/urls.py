from django.urls import path
from .views import HomePageTest

app_name = 'home'

urlpatterns = [
    path('', HomePageTest.as_view(), name='home_page'),
]