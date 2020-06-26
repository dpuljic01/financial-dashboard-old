import dash_core_components as dcc
import dash_html_components as html

layout = html.Div([
    html.Img(
        src="https://i.kym-cdn.com/photos/images/newsfeed/001/499/826/2f0.png",
        style={
            "display": "block",
            "margin": "20px auto",
            "width": "150px",
        }
    ),
    dcc.Dropdown(
        id="my-dropdown",
        options=[
            {"label": "Coke", "value": "COKE"},
            {"label": "Tesla", "value": "TSLA"},
            {"label": "Nio", "value": "NIO"},
            {"label": "Apple", "value": "AAPL"},
            {"label": "CDEV", "value": "CDEV"},
        ],
        value="COKE"
    ),
    dcc.Graph(id="my-graph")
], style={"width": "500"})
