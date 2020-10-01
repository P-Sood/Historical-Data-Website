from celery import shared_task
from django.db import connection
# import the function that needs to be run here 


@shared_task(bind = True)
def NewScraper(self, search ):
    #context = run(search)
    # Run function
    context = 1
    return context
    

