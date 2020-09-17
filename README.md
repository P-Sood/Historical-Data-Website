# Historical-Data-Website

This repository works off of the Backend-Data-Website. I have created a project in Python using both Django and MongoDB, 
in where I scrape data off of Social Media websites using API's.

On the website itself you are able to add data to the database using a search term. 
Once user wants to get the data, you can then query the database and get a CSV file containing the most important aspects of the data. 

Celery for Windows:
celery -A djangoWebsite worker -l info -P gevent

Celery for Mac:
celery -A djangoWebsite worker -l info

Weird error where if the celery queue seems to be stuck, just do a quick search of the database for a csv file and it'll somehow fix it. I think its more to do that the computer gets stuck so the change from getting tweets to querying them allows it to get unstuck
