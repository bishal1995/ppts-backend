from django.conf.urls import url
import views

urlpatterns = [
    url(r'^guard/login/$', views.guard_login),
    url(r'^guard/logout/$', views.guard_logout),
    url(r'^guard/recieve/$', views.recieve_cordinates),
]

