from django.urls import path
from . import views as search_views


urlpatterns = [
    path('' , search_views.home , name = 'search-home'),
    path('tips/' , search_views.tips , name = 'search-tips'),
    #path('download-csv/' , views.downloadCSV , name = 'search-post'),
]