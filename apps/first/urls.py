from django.conf.urls import url
from . import views

app_name="routes"
urlpatterns = [
    url(r'^routes$', views.index, name="index"),
    url(r'^process$', views.process, name="process")
]