from BackEnd_Twitter.TwitterAPITweepy import TwitterAPITweepy
from BackEnd_Twitter.database import DataBase
import BackEnd_Twitter.backend_config as config
from .models import Twitter_data
from celery import shared_task

@shared_task
def queryTweet_Tweepy(search , fromDate, toDate, count ):
    consumer_key = config.Twitter['Consumer_Key']
    consumer_secret = config.Twitter['Consumer_Secret']
    access_token = config.Twitter['Access_Token']
    access_token_secret = config.Twitter['Access_Secret']
    search = [search]

    UserName = config.MongoDB['UserName']
    Password = config.MongoDB['Password']
    database = config.MongoDB['Database']
    collection = config.MongoDB['Collection']

    mongoDB = DataBase(UserName,Password,database,collection)
    api = TwitterAPITweepy(consumer_key,consumer_secret,access_token,access_token_secret,mongoDB)
    api.tweetsDjango_database(search,since=fromDate, until=toDate,count = count)
    return None

