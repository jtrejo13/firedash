# -*- coding: utf-8 -*-

import json

from db.api import find

# Constants
CANTERA_GASES = ['CO2', 'CO', 'H2', 'CH4', 'C2H4', 'C2H6', 'C3H8', 'N2', 'O2',
                 'CH3OH']
# Air composition
AIR_SPECIES = {'O2': 1, 'N2': 3.76}
# Main collection name
MAIN_COLLECTION = 'main'


def _add_search_filter(search=None):
    """ Add filter to ensure presence of CO2, H2, CH4 or C3H8. """
    search_filter = {
        "$and": [
            {"$or": [{'Gases.CO2': {'$gt': 0}}, {'Gases.H2': {'$gt': 0}},
                     {'Gases.CH4': {'$gt': 0}}, {'Gases.C3H8': {'$gt': 0}}]}
        ]
    }
    if search:
        search_filter['$and'].append(search)

    return search_filter


def make_options(values):
    """ Create list of options from list of values. """
    options = []
    for value in values:
        label = 'N/A' if value == '' else value
        options.append({'label': label, 'value': value})
    return options


def get_main_data():
    """ Get data in main collection in JSON serialized form. """
    search = _add_search_filter()
    cols = {'Publication': 1, 'Format': 1, 'Chemistry': 1, 'Electrolyte': 1,
            'SOC': 1, '_id': 0}
    results = find(collection=MAIN_COLLECTION, search=search, projection=cols)
    data = json.dumps(list(results))
    return data
