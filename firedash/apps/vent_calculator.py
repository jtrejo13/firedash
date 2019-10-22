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
                            id='ref_year',
                            options=[],
                            multi=True,
                            value=[],
                            className="dcc_control"
                        ),
                        html.P(
                            'Cell type:',
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
                            'Cell chemistry:',
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
                            'Cell electrolyte:',
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
                            'Cell SOC:',
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
