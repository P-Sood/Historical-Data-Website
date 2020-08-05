from .models import Twitter_data
from .runTweepy import runTweepy
from django.shortcuts import render
from django.template import RequestContext

import csv
from django.http import HttpResponse

from .forms import Search

def home(request):

    homeHTML = 'search/home.html'

    def get(self,request):
        form = Search()
        return render(request,homeHTML)

    def post(self,request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
        # create a form instance and populate it with data from the request:
            form = Search(request.POST)
        # check whether it's valid:
            if form.is_valid():
                query = form.cleaned_data['query']
                toDate_ = form.cleaned_data['toDate']
                fromDate_ = form.cleaned_data['fromDate']
                runTweepy().queryTweet_Tweepy(query,fromDate_,toDate_)
        return render(request, homeHTML,{'form': form})

    def downloadCSV(self,request):
        if(request.GET.get('mybtn')):
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['_id','user_id','date','is_retweet','is_thread','text','emoji','media','likes','retweets','related_hashtags','external_links','tweet_link','search_term'])

            for tweet in Twitter_data.objects.all():
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

                response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

            return response


    context = {
        'Tweets': Twitter_data.objects.all(),
    }
    return render(request,homeHTML,context)

def tips(request):
    return render(request, 'search/tips.html')