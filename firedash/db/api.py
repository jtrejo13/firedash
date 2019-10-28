# -*- coding: utf-8 -*-

import os

from pymongo import MongoClient


DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URI = (f'mongodb://trejo:{DB_PASSWORD}@ds333238.mlab.com:33238'
          '/heroku_2c1mks3g?retryWrites=false')
DB_NAME = 'heroku_2c1mks3g'


def get_unique(collection, field, search={}):
    """ Get all unique items for a field in a given collection.

    Returns
    -------
    List
        List of unique fields in the database.
    """
    client = MongoClient(DB_URI)
    db = client[DB_NAME]

    return db[collection].find(search).distinct(field)
