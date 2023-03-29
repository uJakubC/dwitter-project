from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CreateUserForm()
        context = {'form': form}
        return render(request=request, template_name='register.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)
                return redirect('login')
            except:
                HttpResponseBadRequest("Bad request")
        else:
            messages.error(request, "Somme error occurred during registration :(  -  Please try again")
        form = CreateUserForm()
        context = {'form': form}
        return render(request=request, template_name='register.html', context=context)


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = AuthenticationForm()
        context ={'form': form}
        return render(request=request, template_name='login.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            return redirect('tweet-list')
        else:
            messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        context = {'form': form}
        return render(request=request, template_name='login.html', context=context)


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            messages.error(request, "You are not logged in!")
            return redirect('main-page')
        logout(request)
        messages.info(request, f"Logged out!")
        return redirect('login')


class UserProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name='profile.html', context={})
