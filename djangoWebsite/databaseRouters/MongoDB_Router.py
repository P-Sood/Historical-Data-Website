from django.db import models
class MongoDB_Router:  
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read Twitter_JSON models go to MongoDB.
        """
        if model._meta.app_label == 'twitterjson':
            return 'MongoDB'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write Twitter_JSON models go to MongoDB.
        """
        if model._meta.app_label == "twitterjson":
            return 'MongoDB'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the Twitter_JSON only appears in the 'MongoDB'
        database.
        """
        if app_label == 'twitterjson':
            return db == 'MongoDB'
        return None