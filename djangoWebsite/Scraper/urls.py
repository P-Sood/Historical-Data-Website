from django.urls import path
from . import views as news_views


urlpatterns = [
    path('News/' , news_views.ScrapeNews , name = 'news-scraper'),
]

# local:8000/Scraper