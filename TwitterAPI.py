import tweepy
import re
import csv
import sys
from datetime import date
import json
import os
import glob
import pandas as pd
import pymongo

# Tweepy and Twurl tweet JSON format is different
# Tweepy and Twurl have the same attributes you just get them differently
# Tweepy uses dot method and Twurl uses indexing 

class cleanTweets():

    def __init__(self):
        pass

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
        tweet = re.sub(r'http\S+\s*', '', tweet)  # remove URLs
        tweet = re.sub(r'RT|cc', '', tweet)  # remove RT and cc
        tweet = re.sub(r'#\S+', '', tweet)  # remove hashtags
        # tweet = re.sub(r'@\S+', '', tweet)  # remove mentions
        tweet = re.sub(r'[%s]' % re.escape(r"""!"$%&'()*+,-./:;<=>?[\]^_`{|}~#"""), '', tweet)  # remove punctuations// iF YOU comment out mentions make sure to take out the '@' symbol from here
        tweet = re.sub(r'\s+', ' ', tweet)  # remove extra whitespace
        return tweet

    
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



class TwitterAPITwurl(cleanTweets):

    def __init__(self,path,input_directory,output_directory):
        self.path = path
        self.input_directory = input_directory
        self.output_directory = output_directory

        self.next_count = 0

    def firstTwurlCMD(self,textFileName,csvFileName):
        os.chdir(os.path.join(self.path,self.input_directory))
        cmd = 'twurl \"/1.1/tweets/search/30day/Test.json\" -A \"Content-Type: application/json\" -d \'{\"query\":\"#TwitchBlackout lang:en\",\"maxResults\":\"100\",\"fromDate\":\"202006230000\",\"toDate\":\"202007142359\"}\' > '  + textFileName + ".txt"
        os.system(cmd)
        self.tweets_JSONtoCSV(textFileName,csvFileName)

    # After doing a tweet search in Twurl, you can save it to a text file, and then run this function
    # To put it in a similar format as up above in csv
    def tweets_JSONtoCSV(self,textFileName,csvFileName):
        self.next_count += 1
        # Get Text from the input directory 
        os.chdir(os.path.join(self.path,self.input_directory))
        textFile = open(textFileName + ".txt" , 'r',encoding="utf-8")
        data = json.load(textFile)

        # Put csv in the output directory
        os.chdir(os.path.join(self.path,self.output_directory))
        csvFile = open(csvFileName + ".csv", 'w',encoding="utf-8")
        fieldnames = ['user_id','date','twitter_id','text','media','likes','retweets','related_hashtags','external_links','tweet_link']
        writer = csv.DictWriter(csvFile,fieldnames=fieldnames) 
        writer.writeheader()

        nextPageRequest = data['next']
        print(nextPageRequest)
        
        # When you query in twurl the data you get changes based on JSON, so for the for-loop if you are getting erros
        # Just do a print(tweet) and put that in an online JSON parser and then play around with that until you know 
        # what the data you're receiving actually is

        for tweet in data['results']:
            parsed_tweet = {}
            user = tweet['user']

            tags = ""
            imgTag = ""
            url_link = ""

            parsed_tweet['user_id'] = user['screen_name']
            parsed_tweet['date'] = str(tweet['created_at']) 
            parsed_tweet['twitter_id'] = tweet['id_str']
            parsed_tweet['tweet_link'] = "https://twitter.com/id/status/" + tweet['id_str']
            try:
                parsed_tweet['text'] = super().remove_emoji(super().clean_tweet(tweet['extended_tweet']['full_text'].encode('utf-8').decode('utf-8')))               
            except:
                parsed_tweet['text'] = super().remove_emoji(super().clean_tweet(tweet['text'].encode('utf-8').decode('utf-8'))) 

            try:
                for hashtag in tweet['retweeted_status']['extended_tweet']['entities']['hashtags']:
                    tags += hashtag['text'] + "-"
                tags = re.sub("[^A-Za-z]", " ", tags)
                parsed_tweet['related_hashtags'] = tags
            except:
                try:
                    for hashtag in tweet['extended_tweet']['entities']['hashtags']:
                        tags += hashtag['text'] + "-"
                    tags = re.sub("[^A-Za-z]", " ", tags)
                    parsed_tweet['related_hashtags'] = tags
                except:
                    for hashtag in tweet['entities']['hashtags']:
                        tags += hashtag['text'] + "-"
                    tags = re.sub("[^A-Za-z]", " ", tags)
                    parsed_tweet['related_hashtags'] = tags

            # Next block of code checks to see if tweet has a video, print link. If not check if tweet has multiple images, print img links, 
            # if not then check if just 1 media image, print img, if nothing then print empty
            try:
                parsed_tweet['media'] = tweet['extended_tweet']['extended_entities']["media"][0]["video_info"]["variants"][0]["url"]
            except:
                try:
                    for image in tweet['extended_tweet']['extended_entities']["media"]:
                        imgTag += image["media_url_https"]+ " "
                    parsed_tweet['media'] = imgTag 
                except:
                    parsed_tweet['media'] = ""
                    # Might be useless in twurl format
                    """
                    try:
                        parsed_tweet['media'] = tweet.entities["media_url_https"]
                    except: 
                        parsed_tweet['media'] = ""
                    """
            # Here i have just gone thru some differences that appear if the tweet is a retweet or not

            try:
                parsed_tweet['retweets'] = tweet['retweeted_status']['retweet_count'] 
                parsed_tweet['likes'] =  str(tweet['retweeted_status']['favorite_count']) 
                # If a retweet, 1 link is to direct back to the original tweet, so i ignored it and started at 1
            except:
                parsed_tweet['retweets'] = str(tweet['retweet_count']) 
                parsed_tweet['likes'] =  str(tweet['favorite_count']) 
                
            
            try:
                listAddedLinks = re.findall(r'http\S+\s*', tweet['retweeted_status']['extended_tweet']['full_text'])
                for i in range(1,len(listAddedLinks)):
                    url_link += listAddedLinks[i]
                parsed_tweet['external_links'] = url_link
            except:
                try:
                    for links in re.findall(r'http\S+\s*', tweet['extended_tweet']['full_text']):
                        url_link += links
                    parsed_tweet['external_links'] = url_link 
                except:
                    for links in re.findall(r'http\S+\s*', tweet['text']):
                        url_link += links
                    parsed_tweet['external_links'] = url_link
            writer.writerow(parsed_tweet)
        textFile.close()

        if ( nextPageRequest != None):
            # Both file names will be in format 'search'_i.xxx where search is the term we searched and i is number of times we ran it
            textFileName = textFileName[0:len(textFileName)-2] + "_" + str(self.next_count)
            csvFileName = csvFileName[0:len(csvFileName)-2] + "_" + str(self.next_count)
            self.getNextTweets_fromTwurl(nextPageRequest,textFileName,csvFileName)
        else:
            return

    def getNextTweets_fromTwurl(self,Next,TextFileName,csvFileName):
        os.chdir(os.path.join(self.path,self.input_directory))
        cmd = 'twurl \"/1.1/tweets/search/30day/Test.json\" -A \"Content-Type: application/json\" -d \'{\"query\":\"#TwitchBlackout lang:en\",\"maxResults\":\"100\",\"fromDate\":\"202006230000\",\"toDate\":\"202007142359\",\"next\":' + Next + '}\' > '  + TextFileName + ".txt"
        os.system(cmd)
        self.tweets_JSONtoCSV(TextFileName,csvFileName)
    
    def AppendCSVs(self,combinedFileName,directory,extension):
        os.chdir(directory)
        #find all csv files in the folder
        #use glob pattern matching -> extension = 'csv'
        #save result in list -> all_filenames
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
        #print(all_filenames)

        #combine all files in the list
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
        #export to csv
        combined_csv.to_csv( combinedFileName, index=False, encoding='utf-8')    

  

def main():
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''
    search = "#beaver"

    #api = TwitterAPITweepy(consumer_key,consumer_secret,access_token,access_token_secret)
    #api.get_tweets_tweepy(csvFileName = "tweets_"+ search + ".csv" , searchParameters = [search],count=2)

    Folder = "InputandOutput"

    path = os.path.join(os.getcwd(),Folder)

    input_directory = "input"
    output_directory = "output"

    twurl = TwitterAPITwurl(path,input_directory,output_directory)
            # use file names to be #TwitchBlackout_0.txt and then increment the 0 on both
    twurl.firstTwurlCMD(textFileName = "#TwitchBlackout_0", csvFileName = "#TwitchBlackout_0")
    #twurl.AppendCSVs("Animal.csv","Test_AppendFunction","csv")

if __name__ == "__main__":
    main()



 
