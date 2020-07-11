import tweepy
import re
import csv
from hatebase import HatebaseAPI
import mariadb 

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Here I make the O-Auth to access twitter from my app, and then set its access token

try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
except tweepy.TweepError:
    print("Something is wrong with one of your keys from twitter")


def get_tweets(query, count = 300):

    tweets = []
    searchParameters = ["#BlackOutTuesday"] # If you add to this list, you are using "and" logical operator
    csvFile = open("myCSV.csv", 'w')
    fieldnames = ['name','date','id','text','likes','retweets','related_tags','tweet_link']
    writer = csv.DictWriter(csvFile,fieldnames=fieldnames)
    writer.writeheader()

    # If you want to add another field to the csv file, follow code below and then put it in fieldnames as well 

    for tweet in tweepy.Cursor(api.search,q=searchParameters,count= count,lang="en",since="2020-06-12", until = "2020-06-20" ,tweet_mode="extended",).items():
        parsed_tweet = {}
        user =  tweet.user
        # Making sure there is no link and then adding keys to my dictionary with specific values to be written to csv
        if "http" not in tweet.full_text:
            tags = ""
            tag = " empty "

            # Need to use re library to get a regular expression and not the weird way the text of a tweet is 
            line = re.sub("[^A-Za-z]", " ", tweet.full_text)
            parsed_tweet['id'] = " " + tweet.id_str + " "
            parsed_tweet['name'] = " " + user.screen_name + " "
            parsed_tweet['retweets'] = " " + str(tweet.retweet_count) + " "
            parsed_tweet['tweet_link'] = " https:://twitter.com/id/status/" + tweet.id_str + " "
            parsed_tweet['date'] = " " + str(tweet.created_at) + " "

            # With 240 max characters, this loop is O(120) // 120 number symbol characters and 120 alphanumeric characters that are the hashtag
            # Actuality max is like 10, but not every tweet has it
            for hashtag in tweet.entities['hashtags']:
                tags += hashtag['text'] + "-"
                tag = re.sub("[^A-Za-z]", " ", tags)
            parsed_tweet['related_tags'] = tag

            # Might want to check content of retweet instead of the retweeted status 

            try:
                retweetText = re.sub("[^A-Za-z]", " ", tweet.retweeted_status.full_text)
                parsed_tweet['text'] = " " + retweetText + " "
                parsed_tweet['likes'] = " " + str(tweet.retweeted_status.favorite_count) + " "
            except:
                parsed_tweet['text'] = " " + line + " "
                parsed_tweet['likes'] = " " + str(tweet.favorite_count) + " "                
        

            writer.writerow(parsed_tweet)
    return tweets 

    # creating object of TwitterClient Class
    # calling function to get tweets
tweets = get_tweets(query =" ", count = 1)




