import tweepy
import re
import csv
import os
from datetime import date
from cleanTweets import cleanTweets
from database import DataBase
import backend_config as config
from urllib.parse import urlparse

# Tweepy and Twurl tweet JSON format is different
# Tweepy and Twurl have the same attributes you just get them differently
# Tweepy uses dot method and Twurl uses indexing 

    
class TwitterAPITweepy(cleanTweets,DataBase):
    
    def __init__(self,consumer_key,consumer_secret,access_token,access_token_secret):#,database):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        #self.database = database


    def Auth(self):
        try:
            self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            self.auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tweepy.API(self.auth,wait_on_rate_limit=True)
        except tweepy.error.TweepError:
            print("Something is wrong with one of your keys from Twitter")    
        try:
            self.database.connection()
        except:
            print("Something is wrong with one of your keys from MongoDB") 

        # if you add terms to the searchParams list, it will use the logical and gate
    def get_tweets_tweepy(self,csvFileName, searchParameters , since = "2020-01-01" , until = str(date.today()), count = 5):

        self.Auth()

        lenSearch = len(searchParameters)
    
        tweets = []
        csvFile = open(csvFileName, 'w',encoding="utf-8",newline="")
        fieldnames = ['_id','user_id','date','is_retweet','text','emoji','media','likes','retweets','related_hashtags','external_links','tweet_link','search_term']
        writer = csv.DictWriter(csvFile,fieldnames=fieldnames) 
        writer.writeheader()

        query = []
        for i in range(lenSearch):
            query.append(searchParameters[i].lower())

        # If you want to add another field to the csv file, follow code below and then put it in fieldnames as well 

        for tweet in tweepy.Cursor(self.api.search,q=searchParameters,count= count,lang="en",since = since, until = until ,tweet_mode="extended",).items():
            user =  tweet.user
            # Making sure there is no link and then adding keys to my dictionary with specific values to be written to csv            
            parsed_tweet = {
                '_id':  tweet.id_str,
                'user_id':  user.screen_name,
                'date': str(tweet.created_at),
                'text': super().clean_tweet(super().remove_emoji(tweet.full_text)).strip(),
                'emoji': super().get_emoji(tweet.full_text),
                'related_hashtags': [],
                'search_term': searchParameters,
                }

            # With 240 max characters, this loop is O(120) // 120 number symbol characters and 120 alphanumeric characters that are the hashtag
            # In actuality max is like 10, but not every tweet has it
            for hashtag in tweet.entities['hashtags']:
                related_hashtags = "#" + hashtag['text']
                if (related_hashtags.lower() not in query):
                    parsed_tweet['related_hashtags'].append(related_hashtags)
            

            # The retweeted tweet has the actual likes of the tweet, tweets that are retweets usually have 0 likes and hold no info
            # links are just links that the user puts inside of their text, used regex to find it
            try:
                parsed_tweet['likes'] = str(tweet.retweeted_status.favorite_count) 
                parsed_tweet['tweet_link'] = "https://twitter.com/id/status/" + tweet.id_str 
                parsed_tweet['retweets'] =  str(tweet.retweeted_status.retweet_count) 

                parsed_tweet['is_retweet'] = "True"
            except:
                parsed_tweet['likes'] =  str(tweet.favorite_count) 
                parsed_tweet['tweet_link'] = "https://twitter.com/id/status/" + tweet.id_str 
                parsed_tweet['retweets'] =  str(tweet.retweet_count) 

                parsed_tweet['is_retweet'] = "False"
            

#            try:
#                listAddedLinks_retweets = re.findall(r'http\S+\s*', tweet.retweeted_status.full_text)
#                listAddedLinks = ""
#            except:
#                listAddedLinks = re.findall(r'http\S+\s*', tweet.full_text)
#                listAddedLinks_retweets = ""
#
#            if (listAddedLinks_retweets != ""):
#                parsed_tweet['external_links'] = []
#                for i in range(len(listAddedLinks_retweets)-1):
#                    parsed_tweet['external_links'].append(super().remove_emoji(listAddedLinks_retweets[i].replace('\n',"")))
#            elif(listAddedLinks != ""):
#                parsed_tweet['external_links'] = []
#                for i in range(len(listAddedLinks)):
#                    parsed_tweet['external_links'].append(super().remove_emoji(listAddedLinks[i].replace('\n',"")))
#            else:
#                parsed_tweet['external_links'] = []
#                parsed_tweet['external_links'].append("")

            try:
                listAddedLinks = super().getExternalLinks(tweet.retweeted_status.full_text)
                parsed_tweet['external_links'] = []
                for i in range(len(listAddedLinks)):
                    url = super().unshorten_url(listAddedLinks[i])
                    x = urlparse(url)
                    if (x.netloc != "twitter.com"):
                        parsed_tweet['external_links'].append(super().remove_emoji(url.replace('\n',"")))
            except:   
                listAddedLinks = super().getExternalLinks(tweet.full_text)
                parsed_tweet['external_links'] = []
                for i in range(len(listAddedLinks)):
                    parsed_tweet['external_links'].append(super().remove_emoji(listAddedLinks[i].replace('\n',"")))

            
            #urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.full_text)
            #urls = re.findall(r'http\S+\s*', tweet.full_text)




                
                        
                        

            # Next block of code checks to see if tweet has a video, print link. If not check if tweet has multiple images, print img links, 
            # if not then check if just 1 media image, print img, if nothing then print empty


            # Something is wrong with this code, even though it was working a while back, So i need to find what underlying issue causes
            # it to not work right now
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

            #self.database.insert_one(parsed_tweet)
            writer.writerow(parsed_tweet)
        return tweets 


def main():
    consumer_key = config.Twitter['Consumer_Key']
    consumer_secret = config.Twitter['Consumer_Secret']
    access_token = config.Twitter['Access_Token']
    access_token_secret = config.Twitter['Access_Secret']
    search = "#Portland"

    UserName = config.MongoDB['UserName']
    Password = config.MongoDB['Password']
    database = config.MongoDB['Database']
    collection = config.MongoDB['Collection']

    mongoDB = DataBase(UserName,Password,database,collection)


    api = TwitterAPITweepy(consumer_key,consumer_secret,access_token,access_token_secret)#,mongoDB)
    api.get_tweets_tweepy(csvFileName = "tweets_"+ search + ".csv" , searchParameters = [search],count=5)

if __name__ == "__main__":
    main()



 
