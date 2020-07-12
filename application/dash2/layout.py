import dash_core_components as dcc
import dash_html_components as html
from application.helpers.components import navigation
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Use `hole` to create a donut-like pie chart
labels_stock = ["NIO", "AAPL", "MSFT", "V"]
values = [35, 15, 20, 30]

pie = go.Pie(labels=labels_stock, values=values, hole=.3, name="Stock", hoverinfo="label+percent+name")
fig = go.Figure(data=[pie])

fig.update_layout(
    uniformtext_minsize=18,
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    title_text="Portfolio Allocation",
)

graph = html.Div(id="dash1-main-graph", className="col-s12 col-m8 offset-m2 col-l6 offset-l3", children=[
    dcc.Graph(id="allocation-pie-chart", config={"scrollZoom": True}, figure=fig)
], style={
    "min-width": "400px",
    "width": "50%",
    "height": "400px",
    "margin": "20px"
})

layout = html.Div(className="container main", children=[
    navigation,
    graph
])
