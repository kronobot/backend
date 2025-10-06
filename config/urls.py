from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.core.files.storage import default_storage

def home(request):
    return HttpResponse("Hello world 🚀")

def error(request):
    raise Exception("Test")

urlpatterns = [
    path("", home),
    path("error/", error),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)