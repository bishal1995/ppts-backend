from django.conf.urls import url
import views

urlpatterns = [

	#Guard APIs
    url(r'^guard/login/$', views.GuardLogin.as_view() ),
    url(r'^guard/logout/$', views.GuardLogout.as_view() ),
    url(r'^guard/recieve/$', views.RecieveCordinates.as_view() ),
    #Officer APIs
    url(r'^officer/login/$', views.OfficerLogin.as_view() ),
    url(r'^officer/logout/$', views.OfficerLogout.as_view() ),
    url(r'^officer/getsessionpath/$', views.GetCordinates.as_view() ),
    url(r'^officer/getname/$', views.NameRecomendation.as_view() ),
    url(r'^officer/getlastlocation/$', views.LastLocation.as_view() ),
    url(r'^officer/getlastsession/$', views.LastSession.as_view() ),
    url(r'^officer/sessiontimestampquery/$', views.SessionTimestampQuery.as_view() ),
    url(r'^officer/locationquery/$', views.LocationQuery.as_view() ),

]