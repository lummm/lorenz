#!/usr/bin/env python3.8

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
import pandas as pd
import plotly.express as px

from lorenz import simulate


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


axis_template = {
    "showbackground": True,
    "backgroundcolor": "#141414",
    "gridcolor": "rgb(255, 255, 255)",
    "zerolinecolor": "rgb(255, 255, 255)",
}

plot_layout = {
    "title": "",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "white"},
    "showlegend": False,
    "plot_bgcolor": "#141414",
    "paper_bgcolor": "#141414",
    "scene": {
        "xaxis": axis_template,
        "yaxis": axis_template,
        "zaxis": axis_template,
        "aspectratio": {"x": 1, "y": 1.2, "z": 1},
        "camera": {"eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
        "annotations": [],
    },
}


def init() -> dash.Dash:
    app = dash.Dash(__name__,
                    # external_stylesheets=external_stylesheets
                    )
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples",
                  "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })
    # df = pd.DataFrame({
    #     "x": [1, 2, 3, 4, 5],
    #     "y": [1, 2, 3, 4, 5],
    #     "z": [1, 2, 3, 4, 5],
    # })
    df = simulate()
    fig = px.scatter_3d(
        df,
        x="x", y="y", z="z",
        color="t",
        size_max=2,
        opacity=0.7
    )
    fig["layout"] = plot_layout
    app.layout = html.Div(children=[
        html.H1(children="Hello!"),
        html.Div(children=[
            html.Div("Test fmk hello "),
            dcc.Input(
                id="my-input",
                value="initial value",
                type="text"),
        ]),
        html.Div(id='my-output'),
        dcc.Graph(id="example-graph",
                  figure=fig)
    ])
    return app


app = init()
server = app.server


@app.callback(
    Output(component_id="my-output", component_property="children"),
    [Input(component_id="my-input", component_property="value")]
)
def update(input_value):
    return f"Output!: {input_value}"


if __name__ == '__main__':
    app.run_server(debug=True)
