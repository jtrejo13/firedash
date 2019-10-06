# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html


layout = html.Div([
    html.H3('Battery Vent Gas Hazard Analysis'),
    html.Div(id='hazard-display-value'),
    dcc.Link('Go to Vent Size Calculator',
             href='/apps/vent_calculator')
])
