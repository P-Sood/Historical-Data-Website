import tweepy
import re
import csv
import os
from datetime import date
import pymongo
from cleanTweets import cleanTweets

# Tweepy and Twurl tweet JSON format is different
# Tweepy and Twurl have the same attributes you just get them differently
# Tweepy uses dot method and Twurl uses indexing 

    
class TwitterAPITweepy(cleanTweets):
    
    def __init__(self,consumer_key,consumer_secret,access_token,access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret


    def Auth(self):
        try:
            self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            self.auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tweepy.API(self.auth,wait_on_rate_limit=True)
        except tweepy.error.TweepError:
            print("Something is wrong with one of your keys from twitter")      

        # if you add terms to the searchParams list, it will use the logical and gate
    def get_tweets_tweepy(self,csvFileName, searchParameters , since = "2020-01-01" , until = str(date.today()), count = 5):

        self.Auth()

        tweets = []
        csvFile = open(csvFileName, 'w',encoding="utf-8")
        fieldnames = ['user_id','date','twitter_id','text','media','likes','retweets','related_hashtags','external_links','tweet_link']
        writer = csv.DictWriter(csvFile,fieldnames=fieldnames) 
        writer.writeheader()

        # If you want to add another field to the csv file, follow code below and then put it in fieldnames as well 

        for tweet in tweepy.Cursor(self.api.search,q=searchParameters,count= count,lang="en",since = since, until = until ,tweet_mode="extended",).items():
            parsed_tweet = {}
            user =  tweet.user
            # Making sure there is no link and then adding keys to my dictionary with specific values to be written to csv
            
            
            tags = ""
            imgTag = ""
            url_link = ""

            parsed_tweet['twitter_id'] =  tweet.id_str
            parsed_tweet['user_id'] =  user.screen_name
            parsed_tweet['retweets'] =  str(tweet.retweet_count) 
            parsed_tweet['date'] = str(tweet.created_at) 

            parsed_tweet['text'] = super().remove_emoji(super().clean_tweet(tweet.full_text)) 

            # With 240 max characters, this loop is O(120) // 120 number symbol characters and 120 alphanumeric characters that are the hashtag
            # In actuality max is like 10, but not every tweet has it
            for hashtag in tweet.entities['hashtags']:
                tags += hashtag['text'] + "-"
            tags = re.sub("[^A-Za-z]", " ", tags)
            parsed_tweet['related_hashtags'] = tags

            

            # The retweeted tweet has the actual likes of the tweet, tweets that are retweets usually have 0 likes and hold no info
            # links are just links that the user puts inside of their text, used regex to find it
            try:
                parsed_tweet['likes'] = str(tweet.retweeted_status.favorite_count) 
                parsed_tweet['tweet_link'] = "https://twitter.com/id/status/" + tweet.id_str 

                listAddedLinks = re.findall(r'http\S+\s*', tweet.retweeted_status.full_text)
                for i in range(1,len(listAddedLinks)):
                    url_link += listAddedLinks[i]
                parsed_tweet['external_links'] = url_link
                

            except:
                parsed_tweet['likes'] =  str(tweet.favorite_count) 
                parsed_tweet['tweet_link'] = "https://twitter.com/id/status/" + tweet.id_str 

                listAddedLinks = re.findall(r'http\S+\s*', tweet.full_text)
                if (len(listAddedLinks)>1):
                    for i in range(len(listAddedLinks)-1):
                        url_link += listAddedLinks[i]
                    parsed_tweet['external_links'] = url_link
                

            # Next block of code checks to see if tweet has a video, print link. If not check if tweet has multiple images, print img links, 
            # if not then check if just 1 media image, print img, if nothing then print empty
            try:
                parsed_tweet['media'] = tweet.extended_entities["media"][0]["video_info"]["variants"][0]["url"]
            except:
                try:
                    for image in tweet.extended_entities["media"]:
                        imgTag += image["media_url_https"]+ " "
                    parsed_tweet['media'] = imgTag 
                except:
                    try:
                        parsed_tweet['media'] = tweet.entities["media_url_https"]
                    except:
                        parsed_tweet['media'] = ""

            
                
            writer.writerow(parsed_tweet)
        return tweets 



# These are example keys, I have since made new keys after this mistake

def main():
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''
    search = "#beaver"

    api = TwitterAPITweepy(consumer_key,consumer_secret,access_token,access_token_secret)
    api.get_tweets_tweepy(csvFileName = "tweets_"+ search + ".csv" , searchParameters = [search],count=2)

if __name__ == "__main__":
    main()



 
