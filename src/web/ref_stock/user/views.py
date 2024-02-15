from django.shortcuts import HttpResponseRedirect, render, reverse
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_GET

from . import forms

class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            login_form = forms.UserLoginForm().render("user/form_snippet.html") # within app directory
            return render(request, "user/login.html", {'login_form': login_form})
        else:
            return HttpResponseRedirect(reverse("reference:index"))

    def post(self, request):
        form = forms.UserLoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _("Login successful"), extra_tags="login")
                return HttpResponseRedirect(reverse("reference:index"))
            else:
                messages.error(request, _("Incorrect username or password"), extra_tags="login")
                return HttpResponseRedirect(request.path)
        else:
            for error in form.errors:
                messages.error(request, error, extra_tags="login")
            return HttpResponseRedirect(request.path)

class RegisterView(View):
    
    def get(self, request):
        register_form = forms.UserRegistrationForm().render("user/form_snippet.html")
        return render(request, "user/register.html", {'register_form': register_form})

    def post(self, request):
        form = forms.UserRegistrationForm(data=request.POST)

        if form.is_valid():
            try:
                user = form.save()
            except ValueError as e:
                for msg in e.args:
                    messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            except:
                messages.error(request, _("An error has occured during registration"))
                return HttpResponseRedirect(request.path)
            messages.success(request, "Successfuly registered")
            return HttpResponseRedirect(request.path)

        else:
            password1 = form.data["password1"]
            password2 = form.data["password2"]
            username = form.data["username"]
            email = form.data["email"]

            for error in form.errors:
                if error == 'email':
                    if get_user_model().objects.filter(email=email).exists():
                        messages.error(request, _("Email is already taken"))
                    else:
                        messages.error(request, _("Invalid email"))
                elif error == 'password2' and password1 == password2:
                    messages.error(request, _("The password is not strong enough"))
                elif error == 'password2' and password1 != password2:
                    messages.error(request, _("The passwords do not match"))
                elif error == 'username':
                    if get_user_model().objects.filter(username=username).exists():
                        messages.error(request, _("Username is already taken"))
                    else:
                        messages.error(request, _("Invalid username" + error))
                else:
                    messages.error(request, _("Invalid form error: " + error))
            return HttpResponseRedirect(request.path)

def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, _("Logout successful"))
        return HttpResponseRedirect(reverse("reference:index"))
    else:
        messages.warning(request, _("User is already logged out"))
        return HttpResponseRedirect(request.path)
