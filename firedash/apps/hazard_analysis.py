# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from .callbacks import *  # noqa
from .layouts import main_dropdowns
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
        main_dropdowns,
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
