from .models import Twitter_data,data
from .tasks import queryTweet_Tweepy
from django.shortcuts import render
from django.template import RequestContext
from Home.models import UserExtensionModel
import numpy

from .runTweepy import queryTweet_TweepyTEST

from django_celery_results.models import TaskResult

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

    currentUser = request.user
    currentUserModelExt = UserExtensionModel.objects.get(user = currentUser)

    Inputform = Search()
    Searchform = Query()
    task_id = None

    if request.method == 'POST':
        Inputform = Search(request.POST)
        if Inputform.is_valid():
            input_ = Inputform.cleaned_data['input_']
            toDate_ = Inputform.cleaned_data['toDate']
            fromDate_ = Inputform.cleaned_data['fromDate']
            count_ = Inputform.cleaned_data['count']
            if( is_date(toDate_) and is_date(fromDate_) ):
                task = queryTweet_Tweepy.delay(input_,fromDate_,toDate_,count_)
                task_id = task.task_id
                                
    if request.method == 'GET':
        Searchform = Query(request.GET)
        if Searchform.is_valid():
            search = Searchform.cleaned_data['searchDB']        
            return downloadCSV(search)    

    context = {
        'Inputform': Inputform,
        "Searchform" : Searchform,
        "task_id": task_id,
        
    }

    return render(request,homeHTML,context)

def results(request):

    # Range = request.POST.get('taskID',None)
    # context = {
    #     'range': Range,
    # }
    currentUser = request.user
    currentUserModelExt = UserExtensionModel.objects.get(user = currentUser)
    task_id = request.POST.get('taskID',None)
    task = TaskResult.objects.all().filter(task_id = task_id)
    task_results = None
    task_args = None
    if task:
        task_results = task[0].result
        task_args = task[0].task_args
        print(task[0].status)
        if task[0].status == "PROGRESS" or task[0].status == "SUCCESS":
            UserExtensionModel.objects.filter(user = currentUser).update(arrayTasksCompleted = currentUserModelExt.arrayTasksCompleted + [TaskResult.objects.all().count()])

    context = {
        'task_id': task_id,
        'task_results': task_results,
        'task_args': task_args,
        "celeryTasksArray":  numpy.unique(numpy.array(UserExtensionModel.objects.get(user = currentUser).arrayTasksCompleted)),
    }

    return render(request, 'search/celeryTasks.html',context)

def downloadCSV(search):
    
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['_id','user_id','date','is_retweet','is_thread','text','emoji','media','likes',
        'retweets','related_hashtags','external_links','tweet_link','search_term'])
    try:
        # We can use either related hashtags, or by search term. Or give people an option

        allData_with_searchTerm = data.objects.all().filter(text__contains = search)
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