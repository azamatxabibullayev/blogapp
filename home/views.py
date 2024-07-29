from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class HomePageTest(LoginRequiredMixin, View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'home_page.html')
        else:
            return render('users:login')