from django.conf.urls import url

from . import views

app_name = 'mainapp'

urlpatterns = [
    url(r'^signup/', views.signup, name='signup'),
    url(r'^createprofile/', views.createprofile, name='createprofile'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^map/', views.map, name='map'),
    url(r'^mymeets/', views.mymeets, name='mymeets'),
    url(r'^', views.login_view, name='login'),
]
