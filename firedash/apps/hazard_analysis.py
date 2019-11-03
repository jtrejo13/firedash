# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from .callbacks import *  # noqa
from .util import get_main_data


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
                            'Battery Vent Gas Hazard Analysis',
                        ),
                    ],
                    id="title",
                    className='one-half column',
                    style={"margin-bottom": "30px"}
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Building Deflagration",
                                        id="building-deflagration"),
                            href="/apps/vent_calculator",
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
                                    id='vent_ref_pub',
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
                html.Div(id='vent_gas_temp', style={'display': 'none'}),
                html.Div(
                    [
                        dcc.Graph(id='composition_plot')
                    ],
                    className='pretty_container four columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='main_plot')
                    ],
                    id="explosionGraphContainer",
                    className="pretty_container eight columns"
                )
            ],
            className="row"
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='pie_graph')
                    ],
                    className='pretty_container seven columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='aggregate_graph')
                    ],
                    className='pretty_container five columns',
                ),
            ],
            className='row'
        ),
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)
