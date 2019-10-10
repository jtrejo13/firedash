# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html


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
                            'Battery Vent Gas Hazard Analysis',
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
                            html.Button("Vent Calculator",
                                        id="vent-calculator"),
                            href="/apps/vent_calculator",
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
                            ('Filter by publication date:'),
                            className="control_label"
                        ),
                        dcc.RangeSlider(
                            id='year_slider',
                            min=1960,
                            max=2017,
                            value=[1990, 2010],
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by cell type:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='cell_types',
                            options=[],
                            multi=True,
                            value=[],
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by cell chemistry:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='cell_chemistries',
                            options=[],
                            multi=True,
                            value=[],
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by cell electrolyte:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='cell_electrolytes',
                            options=[],
                            multi=True,
                            value=[],
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by cell SOC:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='cell_soc',
                            options=[],
                            multi=True,
                            value=[],
                            className="dcc_control"
                        ),
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P("No. of Cells"),
                                        html.H6(
                                            id="cell_text",
                                            className="info_text"
                                        )
                                    ],
                                    id="cells",
                                    className="pretty_container"
                                ),

                            ],
                            id="infoContainer",
                            className="row"
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id='count_graph',
                                )
                            ],
                            id="countGraphContainer",
                            className="pretty_container"
                        )
                    ],
                    id="rightCol",
                    className="eight columns"
                )
            ],
            className="row"
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='main_graph')
                    ],
                    className='pretty_container eight columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='individual_graph')
                    ],
                    className='pretty_container four columns',
                ),
            ],
            className='row'
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
