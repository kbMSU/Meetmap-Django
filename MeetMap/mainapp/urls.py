from django.conf.urls import url

from . import views

app_name = 'mainapp'

urlpatterns = [
    url(r'^signup/', views.signup, name='signup'),
    url(r'^createprofile/', views.createprofile, name='createprofile'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^map/', views.map, name='map'),
    url(r'^get_events/', views.get_events, name='get_events'),
    url(r'^create_event/', views.create_event, name='createevent'),
    url(r'^get_user_details/', views.get_user_details, name='getuserdetails'),
    url(r'^going_to_event/', views.going_to_event, name='goingtoevent'),
    url(r'^not_going_to_event/', views.not_going_to_event, name='notgoingtoevent'),
    url(r'^delete_event/', views.delete_event, name='deleteevent'),
    url(r'^mymeets/', views.mymeets, name='mymeets'),
    url(r'^get_my_events', views.get_my_events, name='get_my_events'),

    url(r'^get_profile/', views.get_profile, name='get_profile'),
    url(r'^', views.login, name='login'),
]
