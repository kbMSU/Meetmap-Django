from django.conf.urls import url

from . import views

app_name = 'mainapp'

urlpatterns = [
    url(r'^signup/', views.signup, name='signup'),
    url(r'^createprofile/', views.createprofile, name='createprofile'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^map/', views.map, name='map'),
    url(r'^get_events/', views.get_events, name='get_events'),
    url(r'^mymeets/', views.mymeets, name='mymeets'),
    url(r'^', views.login, name='login'),
]
