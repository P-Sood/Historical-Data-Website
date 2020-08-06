from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name = 'search-home'),
    path('tips/' , views.tips , name = 'search-tips'),
    #path('download-csv/' , views.downloadCSV , name = 'search-post'),
]