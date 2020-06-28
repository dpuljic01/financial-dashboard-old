import dash_core_components as dcc
import dash_html_components as html
from application.helpers.components import navigation

graph = html.Div([
    dcc.Dropdown(
        id="my-dropdown",
        options=[
            {"label": "Tesla", "value": "TSLA"},
            {"label": "Nio", "value": "NIO"},
            {"label": "Apple", "value": "AAPL"},
            {"label": "CDEV", "value": "CDEV"},
        ],
        value="NIO"
    ),
    dcc.Graph(id="my-graph", config={"scrollZoom": True})
], style={
    "max-width": "100%"
})

layout = html.Div(className="container main", children=[
    navigation,
    graph
])
