from django.urls import path
from .views import winning_correlation_view

app_name = 'ncaa_basketball'

urlpatterns = [
    path('',winning_correlation_view,name='winning-correlation-view'),

]
