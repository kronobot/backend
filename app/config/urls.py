from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from api.api import api
from tasks.api import tasks_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("tasks/", tasks_api.urls),
    path("", include("webapp.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
