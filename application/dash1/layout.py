import dash_core_components as dcc
import dash_html_components as html
from application.helpers.components import navigation

graph = html.Div(id="dash1-main-graph", className="col-s12 col-m8 offset-m2 col-l6 offset-l3", children=[
    dcc.Dropdown(
        id="my-dropdown",
        options=[
            {"label": "Tesla", "value": "TSLA"},
            {"label": "Nio", "value": "NIO"},
            {"label": "Apple", "value": "AAPL"},
            {"label": "CDEV", "value": "CDEV"},
        ],
        value="AAPL"
    ),
    dcc.Graph(id="my-graph", config={"scrollZoom": True})
], style={
    "width": "100%"
})

layout = html.Div(className="container main", children=[
    navigation,
    graph
])
