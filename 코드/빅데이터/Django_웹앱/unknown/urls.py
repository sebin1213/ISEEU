from .views import *
from django.urls import path
from django.conf.urls import url

app_name = 'unknown'

urlpatterns =[
    path('list_month/', index1, name='index1'),
    path('list_week/', index2, name='index2'),
    path('list_day/', index3, name='index3'),
    path('nickname/<int:unknown_id>/', Nickname, name='nickname'),
    path('api/list/<int:unknown_id>/', monthlistAPIView.as_view(), name="list_kospi_api"),
    path('api/list_week/<int:unknown_id>/', weekAPIView.as_view(), name="list_week_api"),
    path('api/list_day/<int:unknown_id>/', dayAPIView.as_view(), name="list_day_api"),
    path('chart/month/<int:unknown_id>/', chartmonthAPIView.as_view(), name="chart_month"),
]