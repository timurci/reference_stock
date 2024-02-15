from django.shortcuts import HttpResponseRedirect, render, reverse

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("reference:index"))
    else:
        return HttpResponseRedirect(reverse("user:login"))


