from djongo import models
from djongo.models import fields

"""
'_id','user_id','date','is_retweet','is_thread','text','emoji','media','likes','retweets','related_hashtags','external_links','tweet_link','search_term'


"""

class data(models.Model):
    _id = models.CharField(max_length=30 , primary_key = True)
    user_id = models.CharField(max_length=30)
    date = models.DateField()
    text = models.CharField(max_length=280)
    emoji = models.CharField(max_length=30)
    likes = models.PositiveIntegerField()
    search_term = models.CharField(max_length=30)


class Twitter_data(models.Model):
    keyData = models.OneToOneField(data,on_delete=models.CASCADE,primary_key=True)
    is_retweet = models.CharField(max_length=5)
    is_thread = models.CharField(max_length=5)
    media = models.CharField(max_length=30)
    retweets = models.CharField(max_length=30)
    related_hashtags = models.CharField(max_length=30)
    external_links = models.TextField()
    tweet_link = models.TextField()


    def __str__(self):
        return self.keyData.user_id
