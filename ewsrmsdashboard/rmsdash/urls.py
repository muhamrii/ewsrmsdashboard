from django.urls import path, re_path
from rmsdash import views
from rmsdash.dash_apps.finished_apps import simpleexample
urlpatterns = [

    # The home page
    path('', views.realtime, name='home'),
    path('realtime-detail/<str:servername>/', views.realtimedetail, name='realtimedetail'),
    path('request-history/<str:servername>/', views.requesthistory, name='requesthistory'),
]