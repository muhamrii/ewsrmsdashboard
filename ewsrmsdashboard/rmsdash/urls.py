from django.urls import path, re_path
from rmsdash import views
from rmsdash.dash_apps.finished_apps import simpleexample
urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('realtimedashboard', views.realtime, name='realtime'),
    path('realtime-detail/<str:servername>/', views.realtimedetail, name='realtimedetail')

]