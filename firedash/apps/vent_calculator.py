# -*- coding: utf-8 -*-

import json

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from db.api import get_unique
from scripts.explosion_model import Explosion, Inputs, Patm
from .util import AIR_SPECIES, CANTERA_GASES, MAIN_COLLECTION


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
                                "margin-bottom": "25px"
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
                html.P(
                    '1) Pick a battery explosion experiment:',
                    style={
                        "font-size": "1.5em",
                        "margin-left": "10px",
                        "margin-bottom": "10px"
                    }
                ),
                html.Div(
                    [
                        html.Label(
                            [
                                'Publication:',
                                dcc.Dropdown(
                                    id='vent_ref_pub',
                                    options=get_publications(),
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'Cell type:',
                                dcc.Dropdown(
                                    id='vent_cell_types',
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'Chemistry:',
                                dcc.Dropdown(
                                    id='vent_cell_chemistry',
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'Electrolyte:',
                                dcc.Dropdown(
                                    id='vent_cell_electrolytes',
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'SOC:',
                                dcc.Dropdown(
                                    id='vent_cell_soc',
                                ),
                            ],
                            className="control_label"
                        ),
                    ],
                    className="pretty_container row",
                    style={
                        'width': '75%',
                    }
                ),
            ]
        ),
        html.Div(
            [
                html.P(
                    '2) Room and vent dimensions:',
                    style={
                        "font-size": "1.5em",
                        "margin-left": "10px",
                        "margin-bottom": "10px"
                    }
                ),
                html.Div(
                    [
                        html.Label(
                            [
                                'Spherical Room Radius:',
                                dcc.Input(
                                    id="vent_room_rad",
                                    type="number",
                                    min=0,
                                    placeholder="Radius (m)",
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'Vent Area:',
                                dcc.Input(
                                    id="vent_area",
                                    type="number",
                                    min=0,
                                    placeholder="Area (m^2)",
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'Vent Drag Coefficient (Cd):',
                                dcc.Input(
                                    id="vent_drag",
                                    type="number",
                                    min=0,
                                    placeholder="Drag Coeff",
                                ),
                            ],
                            className="control_label"
                        ),
                    ],
                    className="pretty_container row",
                    style={
                        'width': '50%',
                    }
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            id="vent_gas_temp",
                            className="pretty_container"
                        ),
                    ],
                    id="infoContainer",
                    className="row"
                ),
                html.Div(
                    [dcc.Graph(id='explosion_plot')],
                    id="explosionGraphContainer",
                    className="pretty_container"
                )
            ],
            id="rightCol",
            className="twelve columns"
        )
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


def _get_fuel_species(gases):
    """ Make all non-Cantera gases Propane (C3H8). """
    fuel_species = gases.copy()

    for gas, quantity in gases.items():
        if gas not in CANTERA_GASES:
            fuel_species['C3H8'] += quantity
            fuel_species.pop(gas)

    return fuel_species


@app.callback(
    Output('vent_cell_types', 'options'),
    [Input('vent_ref_pub', 'value')])
def update_cell_types_dropdown(publication):
    """ Update cell types dropdown based on selected value. """
    search = {'Publication': publication}
    _clean_search_dict(search)
    search = _add_search_filter(search)
    values = get_unique(MAIN_COLLECTION, field='Format', search=search)
    return _make_options(values)


@app.callback(
    Output('vent_cell_chemistry', 'options'),
    [
        Input('vent_ref_pub', 'value'),
        Input('vent_cell_types', 'value')
    ])
def update_cell_chemistry_dropdown(publication, cell_type):
    """ Update cell chemistries dropdown based on selected values. """
    search = {'Publication': publication, 'Format': cell_type}
    _clean_search_dict(search)
    search = _add_search_filter(search)
    values = get_unique(MAIN_COLLECTION, field='Chemistry', search=search)
    return _make_options(values)


@app.callback(
    Output('vent_cell_electrolytes', 'options'),
    [
        Input('vent_ref_pub', 'value'),
        Input('vent_cell_types', 'value'),
        Input('vent_cell_chemistry', 'value')
    ])
def update_cell_electrolyte_dropdown(publication, cell_type, chemistry):
    """ Update cell electrolytes dropdown based on selected values. """
    search = {'Publication': publication, 'Format': cell_type,
              'Chemistry': chemistry}
    _clean_search_dict(search)
    search = _add_search_filter(search)
    values = get_unique(MAIN_COLLECTION, field='Electrolyte', search=search)
    return _make_options(values)


@app.callback(
    Output('vent_cell_soc', 'options'),
    [
        Input('vent_ref_pub', 'value'),
        Input('vent_cell_types', 'value'),
        Input('vent_cell_chemistry', 'value'),
        Input('vent_cell_electrolytes', 'value')
    ])
def update_cell_soc_dropdown(publication, cell_type, chemistry, electrolyte):
    """ Update cell SOC dropdown based on selected values. """
    search = {'Publication': publication, 'Format': cell_type,
              'Chemistry': chemistry, 'Electrolyte': electrolyte}
    _clean_search_dict(search)
    search = _add_search_filter(search)
    values = get_unique(MAIN_COLLECTION, field='SOC', search=search)
    return _make_options(values)


@app.callback(
    Output('vent_gas_temp', 'children'),
    [
        Input('vent_ref_pub', 'value'),
        Input('vent_cell_types', 'value'),
        Input('vent_cell_chemistry', 'value'),
        Input('vent_cell_electrolytes', 'value'),
        Input('vent_cell_soc', 'value')
    ])
def update_gases(publication, cell_type, chemistry, electrolyte, soc):
    """ Update gas data based on dropdown selections. """
    search = {'Publication': publication, 'Format': cell_type,
              'Chemistry': chemistry, 'Electrolyte': electrolyte, 'SOC': soc}
    _clean_search_dict(search)
    search = _add_search_filter(search)
    values = get_unique(MAIN_COLLECTION, field='Gases', search=search)
    gases = values[-1] if values else ''
    return json.dumps(gases)


@app.callback(
    Output("explosion_plot", "figure"),
    [
        Input("vent_gas_temp", "children"),
        Input("vent_room_rad", "value"),
        Input("vent_area", "value"),
        Input("vent_drag", "value"),
    ],
)
def make_explosion_figure(gases, radius, area, drag):
    """ Create explosion plot. """
    gases = json.loads(gases) if gases else {}
    data = []

    if gases and radius and area and drag:

        fuel_species = _get_fuel_species(gases)

        # Gas properties
        gas = Inputs(
            air=AIR_SPECIES,
            fuel=fuel_species,
            phi=1.0,  # Composition
            f=1.0,
            P=Patm,  # Initial Pressure
            T=298,  # Initial unburned gas temperature (K)
            S=0.45
        )

        # Room and Vent geometry
        geom = Inputs(
            R=radius,
            Cd=area,
            Av=drag
        )

        # Control inputs
        cntrl = Inputs(
            tmax=0.35  # Max Time for analysis
        )

        explosion = Explosion(gas=gas, geom=geom, cntrl=cntrl)
        explosion.run()

        data = [
            dict(
                type="scatter",
                mode="lines",
                x=explosion.t,
                y=explosion.P_,
                name="Explosion Pressure Over Time",
                opacity=1,
                hoverinfo="skip",
            )
        ]

    layout = dict(
        title="Pressure Over Time",
        dragmode="select",
        showlegend=False,
        autosize=True,
        xaxis={"title": {"text": "time (s)"}},
        yaxis={"title": {"text": "Pressure (MPa)"}},
    )

    figure = dict(data=data, layout=layout)
    return figure
