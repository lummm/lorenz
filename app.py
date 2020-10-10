#!/usr/bin/env python3.8

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
import pandas as pd
import plotly.express as px

import lorenz


external_stylesheets = [
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://unpkg.com/tachyons@4.12.0/css/tachyons.min.css",
]


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
                    external_stylesheets=external_stylesheets
                    )
    app.layout = html.Div(children=[
        html.Div(className="flex", children=[
            html.Div(className="w-20", children=[
                html.Span("Show system 2"),
                daq.ToggleSwitch(
                    color="#add8e6",
                    id='toggle-sys-2',
                    value=True,
                )
            ]),
            html.Div(className="w-40", children=[
                html.Div(
                    u"\u03C1" + ": " + str("rho value..."),
                    style={"fontSize": "20px"}
                ),
                dcc.Slider(
                    id='rho-slider',
                    min=lorenz.RHO_MIN,
                    max=lorenz.RHO_MAX,
                    value=lorenz.rho,
                    step=lorenz.RHO_STEP,
                ),
            ]),
            html.Div(className="w-40", children=[
                html.Div(
                    u"\u03B2" + ": " + str("beta value..."),
                    style={"fontSize": "20px"}
                ),
                dcc.Slider(
                    id='beta-slider',
                    min=lorenz.BETA_MIN,
                    max=lorenz.BETA_MAX,
                    value=lorenz.beta,
                    step=lorenz.BETA_STEP,
                )]
            ),
        ]),
        html.Div(id='my-output'),
        dcc.Graph(id="graph",
                  style={
                      "height": "90vh",
                  })
    ])
    return app


app = init()
server = app.server


def gen_graph(
        rho,
        beta,
        show_sys_2
):
    df = lorenz.simulate(
        rho=rho,
        beta=beta,
        initial=[1.0, 1.0, 100.0]
    )
    df["initial"] = "1"
    if show_sys_2:
        df_2 = lorenz.simulate(
            rho=rho,
            beta=beta,
            initial=[1.0, 1.0, 1.0]
        )
        df_2["initial"] = "2"
        df = pd.concat((df, df_2))
    fig = px.scatter_3d(
        df,
        x="x", y="y", z="z",
        color="initial",
        size="t",
        size_max=20,
        opacity=0.3,
    )
    fig["layout"] = plot_layout
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('graph', 'figure'),
    [Input(component_id="rho-slider", component_property="value"),
     Input(component_id="beta-slider", component_property="value"),
     Input(component_id="toggle-sys-2", component_property="value"),]
)
def update_graph(rho, beta, show_sys_2):
    print(f"rho: {rho}, beta: {beta}, toggle: {show_sys_2}")
    return gen_graph(rho, beta, show_sys_2)


if __name__ == '__main__':
    print("--------- RUNNING DEV SERVER -----------")
    app.run_server(debug=True)
