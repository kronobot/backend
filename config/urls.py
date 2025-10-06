from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.core.files.storage import default_storage

def home(request):
    return HttpResponse("Hello world 🚀")

def test_storage(request):
    return HttpResponse("Your storage is " + str(default_storage.__class__))

urlpatterns = [
    path("", home),
    path("test_storage/", test_storage),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)