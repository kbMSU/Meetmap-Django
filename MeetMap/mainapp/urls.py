from django.conf.urls import url

from . import views

app_name = 'mainapp'

urlpatterns = [
    url(r'^signup/', views.signup, name='signup'),
    url(r'^main/', views.main, name='main'),
    url(r'^createprofile/', views.createprofile, name='createprofile'),
    url(r'^', views.login, name='login'),
]
