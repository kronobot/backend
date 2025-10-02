from django.http import HttpResponse
from django.urls import path
from django.contrib import admin


def home(request):
    return HttpResponse("Hello, world desde Django en Google App Engine 🚀")

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
]