from .models import Twitter_data,data
from .tasks import queryTweet_Tweepy
from django.shortcuts import render
from django.template import RequestContext

from .runTweepy import queryTweet_TweepyTEST

import csv
from django.http import HttpResponse

from .forms import Search,Query

from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def home(request):

    homeHTML = 'search/home.html'

    Inputform = Search()
    Searchform = Query()
    id = None
 
    if request.method == 'POST':
        Inputform = Search(request.POST)
        if Inputform.is_valid():
            input_ = Inputform.cleaned_data['input_']
            toDate_ = Inputform.cleaned_data['toDate']
            fromDate_ = Inputform.cleaned_data['fromDate']
            count_ = Inputform.cleaned_data['count']
            if( is_date(toDate_) and is_date(fromDate_) ):
                # Need to do another check to see if info is already in the database
                task = queryTweet_Tweepy.delay(input_,fromDate_,toDate_,count_)
                id = task.task_id
    
    if request.method == 'GET':
        Searchform = Query(request.GET)
        if Searchform.is_valid():
            search = Searchform.cleaned_data['searchDB'] 
            return downloadCSV(search)

    context = {
        'Inputform': Inputform,
        "Searchform" : Searchform,
        "task_id": id,
    }

    return render(request,homeHTML,context)

def downloadCSV(search):
    
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['_id','user_id','date','is_retweet','is_thread','text','emoji','media','likes',
        'retweets','related_hashtags','external_links','tweet_link','search_term'])
    try:
        allData_with_searchTerm = data.objects.all().filter(search_term__contains = search)
        for data_ in allData_with_searchTerm:
            tweet = Twitter_data.objects.get(keyData__exact = data_._id)
        #for tweet in Twitter_data.objects.all().filter(related_hashtags__contains = search):
            parsed_tweet = {
                '_id' : tweet.keyData._id,
                'user_id' : tweet.keyData.user_id,
                'date' : tweet.keyData.date,
                'is_retweet' : tweet.is_retweet,
                'is_thread' : tweet.is_thread,
                'text' : tweet.keyData.text ,
                'emoji' : tweet.keyData.emoji,
                'media' : tweet.media,
                'likes' : tweet.keyData.likes,
                'retweets' : tweet.retweets,
                'related_hashtags' : tweet.related_hashtags,
                'external_links' : tweet.external_links,
                'tweet_link' : tweet.tweet_link,
                'search_term' : tweet.keyData.search_term,
            }
            writer.writerow(parsed_tweet.values())
    except:
        parsed_tweet = {  '_id' : "Error"  }
        writer.writerow(parsed_tweet.values())

    response['Content-Disposition'] = "attachment; filename= \"" + search + ".csv\""

    return response

def tips(request):
    return render(request, 'search/tips.html')