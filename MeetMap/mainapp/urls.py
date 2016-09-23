from django.conf.urls import url

from . import views

app_name = 'mainapp'

urlpatterns = [
    url(r'^', views.index, name='index'),
    url(r'^test/', views.test, name='test'),
]
