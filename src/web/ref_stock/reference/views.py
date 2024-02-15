from django.shortcuts import HttpResponse, render
from django.views import View

def index(request):
    return render(request, "reference/index.html")

class NewEntry(View):
    def get(self, request):
        return render(request, "reference/new_entry.html")
    def post(self, request):
        return HttpResponse("NewEntry POST request is unimplemented")

class Search(View):
    def get(self, request):
        return HttpResponse("Search GET request is unimplemented")
    def post(self, request):
        return HttpResponse("Search POST request is unimplemented")
