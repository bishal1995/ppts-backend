from django.conf.urls import url
import views

urlpatterns = [
    url(r'^guard/tlogin/$', views.GuardLogin.as_view() ),
    url(r'^guard/tlogout/$', views.GuardLogout.as_view() ),
    url(r'^guard/trecieve/$', views.RecieveCordinates.as_view() ),
    url(r'^officer/tlogin/$', views.OfficerLogin.as_view() ),
    url(r'^officer/tlogout/$', views.OfficerLogout.as_view() ),
    url(r'^officer/tgetpath/$', views.GetCordinates.as_view() ),

]

