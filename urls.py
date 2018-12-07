from django.conf.urls import url
from . import views

app_name = "halflife"

urlpatterns = [
    url(r'^$', views.Index, name='index'),
    url(r'^api/calculate$', views.Calculate, name='calculate'),
]
