from dash.dependencies import Output


def register_callbacks(dash_app):
    return dash_app

# def register_callbacks(dash_app):
#     @dash_app.callback(Output("allocation-pie-chart", "figure"))
#     def update_graph():
#         return {
#             "data": [{
#                 "x": df.index,
#                 "y": df.Close
#             }],
#             "layout": {"margin": {"l": 40, "r": 0, "t": 20, "b": 30}}
#         }
