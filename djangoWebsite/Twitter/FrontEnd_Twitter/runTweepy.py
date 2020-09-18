from Twitter.BackEnd_Twitter.TwitterAPITweepy import TwitterAPITweepy
import Twitter.BackEnd_Twitter.backend_config as config
from .models import Twitter_data


def queryTweet_TweepyTEST(search , fromDate, toDate, count ):
    consumer_key = config.Twitter['Consumer_Key']
    consumer_secret = config.Twitter['Consumer_Secret']
    access_token = config.Twitter['Access_Token']
    access_token_secret = config.Twitter['Access_Secret']
    search = [search]

    api = TwitterAPITweepy(consumer_key,consumer_secret,access_token,access_token_secret)
    print("Before going into backend")
    api.tweetsDjango_database(search,since=fromDate, until=toDate,count = count)
    print("After going into backend")
