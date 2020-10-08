#from djongo import models as MongoModels
#from djongo.models import fields
#from djongo.models.json import JSONField as MongoDB_JSONField
# pip install djongo for these if we every need mongodb again

from django.db import models
from django.db.models import JSONField

"""
'_id','user_id','date','is_retweet','is_thread','text','emoji','media','likes','retweets','related_hashtags','external_links','tweet_link','search_term'
"""

class data(models.Model):
    _id = models.CharField(max_length=50 , primary_key = True)
    user_id = models.TextField()
    date = models.DateField()
    text = models.TextField()
    emoji = models.TextField()
    likes = models.PositiveIntegerField()
    search_term = models.CharField(max_length=50)

    class Meta:
            db_table = "data"


class Twitter_data(models.Model):
    keyData = models.OneToOneField(data,on_delete=models.CASCADE,primary_key=True)
    is_retweet = models.CharField(max_length=5)
    is_thread = models.CharField(max_length=5)
    media = models.TextField()
    retweets = models.TextField()
    related_hashtags = models.TextField()
    external_links = models.TextField()
    tweet_link = models.TextField()


    class Meta:
            db_table = "twitter_data"

class TwitterJSON(models.Model):
    _id = models.CharField(max_length = 50, primary_key = True)
    json = JSONField()
    #json = MongoModels.JSONField()

    class Meta:
            db_table = "twitter_json"