from django.urls import path

from webapp import views

app_name = "webapp"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("events/year/<int:year>/", views.year_archive, name="year_archive"),
    path("events/<uuid:event_id>/", views.event_detail, name="event_detail"),
]
