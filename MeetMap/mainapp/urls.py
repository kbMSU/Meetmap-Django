from django.conf.urls import url

from . import views

app_name = 'mainapp'

urlpatterns = [
    url(r'^signup/', views.signup, name='signup'),
    url(r'^createprofile/', views.createprofile, name='createprofile'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^map/', views.map, name='map'),
    url(r'^mymeets/', views.mymeets, name='mymeets'),
    url(r'^get_profile/', views.get_profile, name='get_profile'),
    url(r'^', views.login, name='login'),
]
