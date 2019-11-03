# -*- coding: utf-8 -*-

import copy
import json

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from app import app
from .controls import GAS_COLORS, plot_layout
from db.api import get_unique
from scripts.explosion_model import Explosion, Inputs, Patm
from .util import (
    _add_search_filter, AIR_SPECIES, CANTERA_GASES, get_main_data,
    MAIN_COLLECTION, make_options
)


# Create app layout
layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=("/assets/shield.png"),
                            style={
                                "height": "60px",
                                "width": "auto",
                            }
                        )
                    ],
                    id="logo",
                    className='one-third column',
                ),
                html.Div(
                    [
                        html.H3(
                            'Building Deflagration',
                            style={"margin-bottom": "0px"}
                        ),
                        html.H5(
                            'Pressure-Time History',
                        )
                    ],
                    id="title",
                    className='one-half column',
                    style={"margin-bottom": "30px"}
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Hazard Analysis",
                                        id="hazard-analysis"),
                            href="/apps/hazard_analysis",
                            style={"float": "right"}
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
                    id='db_data',
                    children=get_main_data(),
                    style={'display': 'none'}
                ),
                html.Div(
                    [
                        html.Label(
                            [
                                'Publication:',
                                dcc.Dropdown(
                                    id='vent_ref_pub'
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'Cell type:',
                                dcc.Dropdown(
                                    id='vent_cell_types'
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'Chemistry:',
                                dcc.Dropdown(
                                    id='vent_cell_chemistry'
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'Electrolyte:',
                                dcc.Dropdown(
                                    id='vent_cell_electrolytes'
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'SOC:',
                                dcc.Dropdown(
                                    id='vent_cell_soc'
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
                html.Div(id='vent_gas_temp', style={'display': 'none'}),
                html.Div(
                    [
                        dcc.Graph(id='composition_plot')
                    ],
                    className='pretty_container four columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='explosion_plot')
                    ],
                    id="explosionGraphContainer",
                    className="pretty_container eight columns"
                )
            ],
            className="row"
        )
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)


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
    [
        Output('vent_ref_pub', 'options'),
        Output('vent_cell_types', 'options'),
        Output('vent_cell_chemistry', 'options'),
        Output('vent_cell_electrolytes', 'options'),
        Output('vent_cell_soc', 'options')],
    [
        Input('db_data', 'children'),
        Input('vent_ref_pub', 'value'),
        Input('vent_cell_types', 'value'),
        Input('vent_cell_chemistry', 'value'),
        Input('vent_cell_electrolytes', 'value'),
        Input('vent_cell_soc', 'value')
    ])
def update_dropdowns(data, publication, cell_type, chemistry, electrolyte,
                     soc):
    """ Update gas dropdown databa based on selections. """
    df = pd.DataFrame(json.loads(data))

    if publication:
        df = df[df['Publication'] == publication]
    if cell_type:
        df = df[df['Format'] == cell_type]
    if chemistry:
        df = df[df['Chemistry'] == chemistry]
    if electrolyte:
        df = df[df['Electrolyte'] == electrolyte]
    if soc:
        df = df[df['SOC'] == soc]

    fields = ['Publication', 'Format', 'Chemistry', 'Electrolyte', 'SOC']
    results = []
    for field in fields:
        result = list(df[field].unique())
        results.append(make_options(result))
    return results


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
    Output("composition_plot", "figure"),
    [Input("vent_gas_temp", "children")],
)
def make_gas_composition_plot(gases):
    """ Create gas composition plot. """
    gases = json.loads(gases) if gases else {}
    data = []

    if gases:
        fuel_species = _get_fuel_species(gases)

        data = [
            dict(
                type="pie",
                labels=[key for key, val in fuel_species.items() if val > 0],
                values=[val for val in fuel_species.values() if val > 0],
                name="Fuel Species Composition",
                textinfo="label",
                textfont=dict(size="18", color="#FFFFFF"),
                hoverinfo="label+percent",
                marker=dict(colors=[GAS_COLORS[gas] for gas in fuel_species]),
            ),
        ]

    layout = copy.deepcopy(plot_layout)
    layout["title"] = "Fuel Species Composition"
    layout["margin"] = dict(l=30, r=30, b=20, t=40)  # noqa
    layout["legend"] = dict(
        font=dict(color="#777777", size="12"),
        orientation="h",
    )

    figure = dict(data=data, layout=layout)
    return figure


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
                name="Explosion Pressure vs. Time",
                opacity=1,
                hoverinfo="skip",
            )
        ]

    layout = copy.deepcopy(plot_layout)
    layout["title"] = "Pressure vs. Time"
    layout["showlegend"] = False
    layout["xaxis"] = {"title": {"text": "time (s)"}}
    layout["yaxis"] = {"title": {"text": "Pressure"}}

    figure = dict(data=data, layout=layout)
    return figure
