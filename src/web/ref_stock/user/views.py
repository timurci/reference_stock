from django.shortcuts import HttpResponseRedirect, render, reverse
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from . import forms

def loginView(request):

    login_form = forms.UserLoginForm().render("user/form_snippet.html") # within app directory
    register_form = forms.UserRegistrationForm().render("user/form_snippet.html")
    context = {'login_form': login_form, 'register_form': register_form}

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, "user/login.html", context)
        else:
            return HttpResponseRedirect(reverse("reference:index"))
    elif request.method == 'POST':
        if request.POST.get("login"):
            if request.POST["login"] == 'guest':
                return HttpResponseRedirect(reverse("reference:index"))
            else:
                form = forms.UserLoginForm(data=request.POST)

                if form.is_valid():
                    username = form.cleaned_data["username"]
                    password = form.cleaned_data["password"]
                    user = authenticate(request, username=username, password=password)
                    if user != None:
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
        else:
            return Http404(_("Unrecognized submit name"))
    else:
        return Http404(_("Unrecognized request method"))

def registerView(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(data=request.POST)

        if form.is_valid():
            #username = form.cleaned_data["username"]
            #email = form.cleaned_data["email"]

            try:
                user = form.save()
                #get_user_model().objects.create_user(username, email, password)
            except ValueError as e:
                for msg in e.args:
                    messages.error(request, msg)
                return HttpResponseRedirect(reverse("user:login"))
            except:
                messages.error(request, _("An error has occured during registration"))
                return HttpResponseRedirect(request.path)
            messages.success(request, "Successfuly registered", extra_tags="register")
            return HttpResponseRedirect(request.path)

        else:
            password1 = form.data["password1"]
            password2 = form.data["password2"]
            username = form.data["username"]
            email = form.data["email"]

            for error in form.errors:
                if error == 'email':
                    if get_user_model().objects.filter(email=email).exists():
                        messages.error(request, _("Email is already taken"), extra_tags="register")
                    else:
                        messages.error(request, _("Invalid email"), extra_tags="register")
                elif error == 'password2' and password1 == password2:
                    messages.error(request, _("The password is not strong enough"), extra_tags="register")
                elif error == 'password2' and password1 != password2:
                    messages.error(request, _("The passwords do not match"), extra_tags="register")
                elif error == 'username':
                    if get_user_model().objects.filter(username=username).exists():
                        messages.error(request, _("Username is already taken"), extra_tags="register")
                    else:
                        messages.error(request, _("Invalid username" + error), extra_tags="register")
                else:
                    messages.error(request, _("Invalid form error: " + error), extra_tags="register")
            return HttpResponseRedirect(request.path)
    else:
        return HttpResponseRedirect(reverse("user:login"))

def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, _("Logout successful"))
        return HttpResponseRedirect(reverse("reference:index"))
    else:
        messages.warning(request, _("User is already logged out"))
        return HttpResponseRedirect(request.path)
