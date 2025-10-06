from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin


def home(request):
    return HttpResponse("Hello world 🚀")

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)