from django.urls import path
from .views import shot_chart_view,shot_graphs_view

app_name = 'nba'

urlpatterns = [
    path('',shot_chart_view,name='shot-chart-view'),
    path('nba_graphs/',shot_graphs_view,name="shot-graph-view")
]
