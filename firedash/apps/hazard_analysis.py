# -*- coding: utf-8 -*-

import copy
import json

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
from plotly.figure_factory import create_ternary_contour

from app import app
from .callbacks import *  # noqa
from .controls import plot_layout
from .layouts import main_dropdowns
from .util import get_flammability_data, TERNARY_OPTIONS


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
                html.Div(id='selected_experiment', style={'display': 'none'}),
                html.Div(id='gas_composition', style={'display': 'none'}),
                html.Div(id='flammability_data', style={'display': 'none'}),
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
                        html.Label(
                            [
                                'Select variable to plot:',
                                dcc.Dropdown(
                                    id='ternary_dropdown',
                                    options=TERNARY_OPTIONS,
                                    style={'width': '60%'},
                                ),
                            ],
                            className="control_label"
                        ),
                        dcc.Graph(id='ternary_graph')
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


@app.callback(
    Output('flammability_data', 'children'),
    [Input('selected_experiment', 'children')])
def update_flammability_data(experiment):
    """ Load experiment data based on selected experiment. """
    data = None
    if experiment:
        data = get_flammability_data(json.loads(experiment))

    return data


@app.callback(
    Output('ternary_graph', 'figure'),
    [
        Input('flammability_data', 'children'),
        Input('ternary_dropdown', 'value'),
    ])
def make_ternary_plot(flammability_data, dropdown_value):
    """ Make ternary graph from flammability data. """
    data = []

    if flammability_data and dropdown_value:
        flammability_data = json.loads(flammability_data)

        xf = flammability_data['Xf']
        xa = flammability_data['Xa']
        xi = flammability_data['Xi']
        z = np.array(flammability_data[dropdown_value])

        colorscale = 'Hot'
        ncontours = None
        showscale = True

        if dropdown_value == 'phi':
            # Cap phi values at 2
            for i, value in enumerate(z):
                if value > 2:
                    z[i] = 2

            ncontours = 8
            colorscale = 'Rainbow'

        if dropdown_value == 'Flammable':
            ncontours = 2
            showscale = False

        figure = create_ternary_contour(np.array([xf, xa, xi]), z,
                                        pole_labels=['Fuel', 'Air', 'Inert'],
                                        interp_mode='cartesian',
                                        colorscale=colorscale,
                                        showscale=showscale,
                                        ncontours=ncontours)

        data = figure.to_plotly_json()['data']

        # Clean up
        for item in data:
            item.pop('showlegend', None)

    layout = copy.deepcopy(plot_layout)
    layout['title'] = 'Ternary Contour Plot'
    layout['showlegend'] = False
    layout['ternary'] = dict(
        sum=1,
        aaxis=dict(title='Fuel'),
        baxis=dict(title='Air'),
        caxis=dict(title='Inert'),
        showlegend=False,
        width=700,
    )

    figure = dict(data=data, layout=layout)
    return figure
