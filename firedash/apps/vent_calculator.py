# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from db.api import get_unique

DB_COLLECTION = 'main'


def get_drowpdown_years():
    """ Get fields for year dropdown. """
    years = sorted(get_unique(collection=DB_COLLECTION, field='Year'))
    return [{'label': str(year), 'value': year} for year in years]


# Create app layout
layout = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src=("https://www.nicepng.com/png/full/832-8326149_shield"
                         "-university-of-texas-at-austin-mechanical-"
                         "engineering.png"),
                    className='one-third column',
                    style={
                        "height": "60px",
                        "width": "auto",
                        "margin-bottom": "25px"
                    }
                ),
                html.Div(
                    [
                        html.H3(
                            'Vent Calculator',
                            style={
                                "margin-tom": "0px",
                                "margin-bottom": "0px"
                            }
                        ),
                        html.H5(
                            'Fire Research Group',
                            style={
                                "margin-bottom": "0px"
                            }
                        )
                    ],
                    id="title",
                    className='one-half column'
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Hazard Analysis",
                                        id="hazard-analysis"),
                            href="/apps/hazard_analysis",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className='row flex-display',
            style={
                "magin-bottom": "25px"
            }
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ('Publication date:'),
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='vent_ref_year',
                            options=get_drowpdown_years(),
                            className="dcc_control"
                        ),
                        html.P(
                            ('Publication author:'),
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='vent_ref_author',
                            className="dcc_control"
                        ),
                        html.P(
                            'Cell type:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='vent_cell_types',
                            className="dcc_control"
                        ),
                        html.P(
                            'Cell chemistry:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='vent_cell_chemistry',
                            className="dcc_control"
                        ),
                        html.P(
                            'Cell electrolyte:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='vent_cell_electrolytes',
                            className="dcc_control"
                        ),
                        html.P(
                            'Cell SOC:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='vent_cell_soc',
                            className="dcc_control"
                        ),
                    ],
                    className="pretty_container two columns"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    id="dynamic-cells",
                                    className="pretty_container"
                                ),

                            ],
                            id="infoContainer",
                            className="row"
                        ),
                        html.Div(
                            [dcc.Graph(id='explosion_plot')],
                            id="countGraphContainer",
                            className="pretty_container"
                        )
                    ],
                    id="rightCol",
                    className="ten columns"
                )
            ],
            className="row"
        ),
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)


def _make_options(values):
    """ Create list of options from list of values. """
    options = []
    for value in values:
        if value is None:
            value = 'N/A'
        options.append({'label': value, 'value': value})
    return options


def _clean_search_dict(search):
    """ Replace 'N/A' values with None in search dict. """
    for key, value in search.items():
        if value == 'N/A':
            search[key] = None


@app.callback(
    Output('vent_ref_author', 'options'),
    [Input('vent_ref_year', 'value')])
def update_authors_dropdown(year):
    """ Update authors based on selected year. """
    search = {'Year': year}
    _clean_search_dict(search)
    values = get_unique(DB_COLLECTION, field='Reference', search=search)
    return _make_options(values)


@app.callback(
    Output('vent_cell_types', 'options'),
    [
        Input('vent_ref_year', 'value'),
        Input('vent_ref_author', 'value')
    ])
def update_cell_types_dropdown(year, author):
    """ Update cell types dropdown based on selected value. """
    search = {'Year': year, 'Reference': author}
    _clean_search_dict(search)
    values = get_unique(DB_COLLECTION, field='Format', search=search)
    return _make_options(values)


@app.callback(
    Output('vent_cell_chemistry', 'options'),
    [
        Input('vent_ref_year', 'value'),
        Input('vent_ref_author', 'value'),
        Input('vent_cell_types', 'value')
    ])
def update_cell_chemistry_dropdown(year, author, cell_type):
    """ Update cell chemistries dropdown based on selected values. """
    search = {'Year': year, 'Reference': author, 'Format': cell_type}
    _clean_search_dict(search)
    values = get_unique(DB_COLLECTION, field='Chemistry', search=search)
    return _make_options(values)


@app.callback(
    Output('vent_cell_electrolytes', 'options'),
    [
        Input('vent_ref_year', 'value'),
        Input('vent_ref_author', 'value'),
        Input('vent_cell_types', 'value'),
        Input('vent_cell_chemistry', 'value')
    ])
def update_cell_electrolyte_dropdown(year, author, cell_type, chemistry):
    """ Update cell electrolytes dropdown based on selected values. """
    search = {'Year': year, 'Reference': author,
              'Format': cell_type, 'Chemistry': chemistry}
    _clean_search_dict(search)
    values = get_unique(DB_COLLECTION, field='Electrolyte', search=search)
    return _make_options(values)


@app.callback(
    Output('vent_cell_soc', 'options'),
    [
        Input('vent_ref_year', 'value'),
        Input('vent_ref_author', 'value'),
        Input('vent_cell_types', 'value'),
        Input('vent_cell_chemistry', 'value'),
        Input('vent_cell_electrolytes', 'value')
    ])
def update_cell_soc_dropdown(year, author, cell_type, chemistry, electrolyte):
    """ Update cell SOC dropdown based on selected values. """
    search = {'Year': year, 'Reference': author, 'Format': cell_type,
              'Chemistry': chemistry, 'Electrolyte': electrolyte}
    _clean_search_dict(search)
    values = get_unique(DB_COLLECTION, field='SOC', search=search)
    return _make_options(values)
