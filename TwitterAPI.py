import tweepy
import re
import csv
import sys
from datetime import date

class TwitterAPI():
    
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

    def remove_emoji(self,tweet):
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', tweet)

    def clean_tweet(self,tweet):
        tweet = re.sub('http\S+\s*', '', tweet)  # remove URLs
        tweet = re.sub('RT|cc', '', tweet)  # remove RT and cc
        tweet = re.sub('#\S+', '', tweet)  # remove hashtags
        # tweet = re.sub('@\S+', '', tweet)  # remove mentions
        tweet = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?[\]^_`{|}~"""), '', tweet)  # remove punctuations// iF YOU comment out mentions make sure to take out the '@' symbol from here
        tweet = re.sub('\s+', ' ', tweet)  # remove extra whitespace
        return tweet


        # if you add terms to the searchParams list, it will use the logical and gate
    def get_tweets(self,csvFileName, searchParameters , since = "2020-01-01" , until = str(date.today()), count = 5):

        self.Auth()

        tweets = []
        csvFile = open(csvFileName, 'w',encoding="utf-8")
        fieldnames = ['user_id','date','twitter_id','text','hyperlinks','likes','retweets','related_hashtags','added_url','tweet_link']
        writer = csv.DictWriter(csvFile,fieldnames=fieldnames) 
        writer.writeheader()

        # If you want to add another field to the csv file, follow code below and then put it in fieldnames as well 

        for tweet in tweepy.Cursor(self.api.search,q=searchParameters,count= count,lang="en",since = since, until = until ,tweet_mode="extended",).items():
            parsed_tweet = {}
            user =  tweet.user
            # Making sure there is no link and then adding keys to my dictionary with specific values to be written to csv
            

            tags = ""
            tag = " empty "
            imgTag = ""
            url_link = ""

            parsed_tweet['twitter_id'] =  tweet.id_str
            parsed_tweet['user_id'] =  user.screen_name 
            parsed_tweet['retweets'] =  str(tweet.retweet_count) 
            parsed_tweet['date'] = str(tweet.created_at) 
            parsed_tweet['text'] = self.remove_emoji(self.clean_tweet(tweet.full_text)) 

            # With 240 max characters, this loop is O(120) // 120 number symbol characters and 120 alphanumeric characters that are the hashtag
            # In actuality max is like 10, but not every tweet has it
            for hashtag in tweet.entities['hashtags']:
                tags += hashtag['text'] + "-"
                tag = re.sub("[^A-Za-z]", " ", tags)
            parsed_tweet['related_hashtags'] = tag

            

            # The retweeted tweet has the actual likes of the tweet, tweets that are retweets usually have 0 likes and hold no info
            # links are just links that the user puts inside of their text, used regex to find it
            try:
                parsed_tweet['likes'] = " " + str(tweet.retweeted_status.favorite_count) + " "
                parsed_tweet['tweet_link'] = " https://twitter.com/id/status/" + tweet.id_str + " "
                for links in re.findall('http\S+\s*', tweet.retweeted_status.full_text):
                    url_link += links
                parsed_tweet['added_url'] = url_link

            except:
                parsed_tweet['likes'] = " " + str(tweet.favorite_count) + " "
                parsed_tweet['tweet_link'] = " https://twitter.com/id/status/" + tweet.id_str + " "
                for links in re.findall('http\S+\s*', tweet.full_text):
                    url_link += links
                parsed_tweet['added_url'] = url_link 

            # Next block of code checks to see if tweet has a video, print link. If not check if tweet has images, print img links, 
            # if not then no media print empty
            try:
                parsed_tweet['hyperlinks'] = tweet.extended_entities["media"][0]["video_info"]["variants"][0]["url"]
            except:
                try:
                    for image in tweet.extended_entities["media"]:
                        imgTag += image["media_url_https"]+ " "
                    parsed_tweet['hyperlinks'] = imgTag 
                except:
                    parsed_tweet['hyperlinks'] = " empty "

            
                
            writer.writerow(parsed_tweet)
        return tweets 


def main():
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    api = TwitterAPI(consumer_key,consumer_secret,access_token,access_token_secret)
    api.get_tweets(csvFileName = "myCSV.csv" , searchParameters = ["#blackouttuesday"])

if __name__ == "__main__":
    main()



 
