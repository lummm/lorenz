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


INPUT_WIDTH = "50px"
ROUTE_PREFIX = "/visual/"

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

GRAPH = dcc.Graph(
    id="graph",
    style={
        "height": "100vh",
        "width": "80vw",
    })

BLURB = html.Div(children=[
    html.Span(children=[
        "These are solutions the system described by the",
        html.Span(className="b", children="Lorenz equations:")
    ]),
    html.Img(src=("https://wikimedia.org/api/rest_v1/media/math/render/svg/"
                  "7928004d58943529a7be774575a62ca436a82a7f")),
])

TOOLBAR_ITEMS = [
    html.Div(className="pr4 f3 b", children="System A"),
    html.Div("Initial point:"),
    html.Div(className="nowrap", children=[
        dcc.Input(id="initial-x", style={"width": INPUT_WIDTH},
                  value="1.0", type="number", step=0.1),
        dcc.Input(id="initial-y", style={"width": INPUT_WIDTH},
                  value="1.0",
                  type="number", step=0.1),
        dcc.Input(id="initial-z", style={"width": INPUT_WIDTH},
                  value="1.0",
                  type="number", step=0.1),
    ]),

    html.Div(className="pr4 f3 b flex justify-between w-100 pt4", children=[
        html.Div(className="nowrap", children="System B"),
        daq.ToggleSwitch(
            color="#add8e6",
            id='toggle-sys-2',
            value=True,
        )]),
    html.Div("Initial point:"),
    html.Div(className="nowrap", children=[
        dcc.Input(style={"width": INPUT_WIDTH},
                  value="1.0", type="number", disabled=True),
        dcc.Input(style={"width": INPUT_WIDTH},
                  value="1.0", type="number", disabled=True),
        dcc.Input(style={"width": INPUT_WIDTH},
                  value="1.0", type="number", disabled=True),
    ]),

    html.Div(className="flex f3 pt4", children=[
        html.Span(className="b pr1",
                  children=u"\u03C3" + ": "),
        html.Span("10.0")
    ]),

    html.Div(className="flex f3", children=[
        html.Span(className="b pr1",
                  children=u"\u03C1" + ": "),
        html.Span(id="rho")
    ]),
    dcc.Slider(
        id='rho-slider',
        min=lorenz.RHO_MIN,
        max=lorenz.RHO_MAX,
        value=lorenz.rho,
        step=lorenz.RHO_STEP,
    ),

    html.Div(className="flex f3", children=[
        html.Span(className="b pr1",
                  children=u"\u03B2" + ": "),
        html.Span(id="beta")
    ]),
    dcc.Slider(
        id='beta-slider',
        min=lorenz.BETA_MIN,
        max=lorenz.BETA_MAX,
        value=lorenz.beta,
        step=lorenz.BETA_STEP,
    ),

    BLURB,
]

LAYOUT = html.Div(className="flex", children=[
    GRAPH,
    html.Div(
        className="flex flex-column white",
        style={"width": "20vw", "backgroundColor": "#141414"},
        children=TOOLBAR_ITEMS),
])


app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                routes_pathname_prefix=ROUTE_PREFIX,
                )
app.layout = LAYOUT
server = app.server


def gen_graph(
        rho,
        beta,
        show_sys_2,
        initial
):
    df = lorenz.simulate(
        rho=rho,
        beta=beta,
        initial=initial
    )
    df["system"] = "A"
    if show_sys_2:
        df_2 = lorenz.simulate(
            rho=rho,
            beta=beta,
            initial=[1.0, 1.0, 1.0]
        )
        df_2["system"] = "B"
        df = pd.concat((df, df_2))
    fig = px.scatter_3d(
        df,
        x="x", y="y", z="z",
        color="system",
        size="t",
        size_max=20,
        opacity=0.3,
    )
    fig["layout"] = plot_layout
    fig.update_layout(transition_duration=500)
    return fig


def format_number(d):
    return "{:.3f}".format(d)


@app.callback(
    Output('graph', 'figure'),
    [Input(component_id="rho-slider", component_property="value"),
     Input(component_id="beta-slider", component_property="value"),
     Input(component_id="toggle-sys-2", component_property="value"),
     Input(component_id="initial-x", component_property="value"),
     Input(component_id="initial-y", component_property="value"),
     Input(component_id="initial-z", component_property="value"),
     ]
)
def update_graph(rho, beta, show_sys_2, x, y, z):
    return gen_graph(rho, beta, show_sys_2, [x, y, z])


@app.callback(
    Output('rho', 'children'),
    [Input(component_id="rho-slider", component_property="value"),]
)
def update_rho(rho):
    return format_number(rho)


@app.callback(
    Output('beta', 'children'),
    [Input(component_id="beta-slider", component_property="value"),]
)
def update_beta(beta):
    return format_number(beta)


if __name__ == '__main__':
    print("--------- RUNNING DEV SERVER -----------")
    app.run_server(debug=True)
