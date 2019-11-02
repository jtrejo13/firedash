# -*- coding: utf-8 -*-

from db.api import get_unique

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


def get_publications():
    """ Get fields for publications dropdown. """
    search = _add_search_filter()
    publications = sorted(get_unique(collection=MAIN_COLLECTION,
                                     field='Publication',
                                     search=search))
    return [{'label': pub, 'value': pub} for pub in publications]
