from .models import Twitter_data,data
from .tasks import queryTweet_Tweepy
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.contrib.messages import error
import json

from Home.models import UserExtensionModel


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


def queryDB(request):

    homeHTML = 'search/queryDB.html'

    Searchform = Query()

    if request.method == 'GET':
        Searchform = Query(request.GET)
        if Searchform.is_valid():
            search = Searchform.cleaned_data['searchDB']        
            return downloadCSV(search)   

    context = {
        "Searchform" : Searchform,        
    }

    return render(request,homeHTML,context)

def addDB(request):

    homeHTML = 'search/addDB.html'

    Inputform = Search()
    task_id = None
    inDatabase = False

    currentUser = request.user
    currentUserModelExt = UserExtensionModel.objects.filter(user = currentUser)

    if request.method == 'POST':
        Inputform = Search(request.POST)
        if Inputform.is_valid():
            input_ = Inputform.cleaned_data['input_']
            toDate_ = Inputform.cleaned_data['toDate']
            fromDate_ = Inputform.cleaned_data['fromDate']
            count_ = Inputform.cleaned_data['count']
            if( is_date(toDate_) and is_date(fromDate_) ):
                taskArgsString = "('" + input_ + "', '" + fromDate_ + "', '" + toDate_ +  "', " + str(count_) + ")"

                for task in TaskResult.objects.all():
                    if taskArgsString == task.task_args:
                        inDatabase = True
                        print("Already there buddy")
                        error(request,"Your exact arguements are already in the database")
                        return redirect('/Twitter/addDB/')

                if not inDatabase:
                    print("Good to go")
                    task = queryTweet_Tweepy.delay(input_,fromDate_,toDate_,count_)
                    task_id = task.task_id
                    numTasks = TaskResult.objects.all().count() + 1
                    currentUserModelExt.update(arrayTasksCompleted = currentUserModelExt[0].arrayTasksCompleted + [numTasks])
                    return redirect("/Twitter/addDB/")
                
    context = {
        'Inputform': Inputform,
        "task_id": task_id,
    }

    return render(request,homeHTML,context)

def results(request):

    arrayTaskArgs = []
    arrayTaskResult = []
    arrayTaskStatus = []

    currentUser = request.user
    currentUserModelExt = UserExtensionModel.objects.filter(user = currentUser)
    currentUserModelExt_arrayTasksCompleted = currentUserModelExt[0].arrayTasksCompleted

    try:
        task_id = TaskResult.objects.filter(id = currentUserModelExt_arrayTasksCompleted[-1])[0].task_id
        print("Did this try/except")
    except IndexError:
        task_id = None


    for taskNumber in currentUserModelExt_arrayTasksCompleted:
        try:
            task = TaskResult.objects.filter(id = taskNumber)[0]

            args = task.task_args
            args =  args[1:len(args)-1].split(',')             
            arrayTaskArgs.append(args)

            result = json.loads(task.result)
            arrayTaskResult.append(result)

            status = task.status
            arrayTaskStatus.append(status)



        except IndexError:
            return redirect('/Twitter/results/')

    context = {
        'task_id': task_id,
        'tasksData' : zip(currentUserModelExt_arrayTasksCompleted,arrayTaskArgs ,arrayTaskResult, arrayTaskStatus),
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