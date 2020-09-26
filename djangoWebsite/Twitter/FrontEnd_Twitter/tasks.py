from Twitter.BackEnd_Twitter.TwitterAPITweepy import TwitterAPITweepy
import Twitter.BackEnd_Twitter.backend_config as config

from .models import Twitter_data
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.db import connection

@shared_task(bind = True)
def queryTweet_Tweepy(self, search , fromDate, toDate, count ):
    consumer_key = config.Twitter['Consumer_Key']
    consumer_secret = config.Twitter['Consumer_Secret']
    access_token = config.Twitter['Access_Token']
    access_token_secret = config.Twitter['Access_Secret']
    

    api = TwitterAPITweepy(consumer_key,consumer_secret,access_token,access_token_secret)

    search = [search]
    context = api.tweetsDjango_database(search,ProgressRecorder(self),since=fromDate, until=toDate,count = count)
    
    #context = api.HIST(searchParameters = search,progressRecorder = ProgressRecorder(self), since = fromDate , until = toDate , count = count)

    return context
    

