from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserForm, ProfileUpdateForm


class RegisterView(View):
    def get(self, request):
        create_form = CustomUserForm()
        context = {'form': create_form}
        return render(request, 'registration/register.html', context=context)

    def post(self, request):
        create_form = CustomUserForm(data=request.POST, files=request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect('login')
        else:
            context = {'form': create_form}
            return render(request, 'registration/register.html', context=context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {'form': login_form}
        return render(request, 'registration/login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
        else:
            context = {'form': login_form}
            return render(request, 'registration/login.html', context=context)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        context = {'user': request.user}
        return render(request, 'registration/profile.html', context=context)


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        update_form = ProfileUpdateForm(instance=request.user)
        return render(request, 'registration/profile_update.html', {'update_form': update_form})

    def post(self, request):
        update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('profile')
        else:
            context = {'update_form': update_form}
            return render(request, 'registration/profile_update.html', context=context)
