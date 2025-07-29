from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("manifest.json", views.manifest, name="manifest"),
    path("service-worker.js", views.service_worker, name="service_worker"),
    path("browserconfig.xml", views.browserconfig, name="browserconfig"),
    path("logout/", views.logout_view, name="logout"),
]
