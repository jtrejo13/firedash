# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html


layout = html.Div([
    html.H3('Building Deflagration Vent Size Calculator'),
    html.Div(id='calculator-display-value'),
    dcc.Link('Go to Battery Vent Gas Hazard Analysis',
             href='/apps/hazard_analysis')
])
