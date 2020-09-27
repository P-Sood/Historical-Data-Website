from django.urls import path
from . import views as search_views


urlpatterns = [
    path('addDB/' , search_views.addDB , name = 'search-addDB'),
    path('queryDB/' , search_views.queryDB , name = 'search-queryDB'),
    path('results/',search_views.results, name = 'search-results')
    #path('download-csv/' , views.downloadCSV , name = 'search-post'),
]