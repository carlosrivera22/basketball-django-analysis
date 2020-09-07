from django.urls import path
from .views import upload_file_view,upload_nba_file_view

app_name = 'csvs'

urlpatterns = [
    path('ncaa_upload/', upload_file_view, name='upload-view'),
    path('nba_upload/', upload_nba_file_view,name='upload-nba-view')
]