import dash_html_components as html

navigation = html.Nav(className="blue darken-4", children=[
    html.Div(className="nav-wrapper container", children=[
        html.A(href="#", className="left", children=[
            html.I("show_chart", className="material-icons")
        ]),
        html.Ul(
            children=[
                html.Li(html.A('Home', href='/')),
                html.Li(html.A('Profile', href='/profile')),
                html.Li(html.A('Dash1', href='/dash1')),
                html.Li(html.A('Dash2', href='/dash2')),
                html.Li(html.A('Logout', href='/logout')),
            ],
            className='hide-on-med-and-down right'
        ),
        html.A(href="#", className="dropdown-trigger right hide-on-large-only", **{"data-activates": "dropdown1"}, children=[
            html.I("menu", className="material-icons")
        ]),
        html.Ul(
            children=[
                html.Li(html.A('Home', href='/')),
                html.Li(className="divider"),
                html.Li(html.A('Profile', href='/profile')),
                html.Li(className="divider"),
                html.Li(html.A('Dash1', href='/dash1')),
                html.Li(className="divider"),
                html.Li(html.A('Dash2', href='/dash2')),
                html.Li(className="divider"),
                html.Li(html.A('Logout', href='/logout')),
            ],
            id='dropdown1',
            className='dropdown-content'
        ),
    ])
])

main = html.Div(className="container main", children=[navigation])

custom_index_string = """
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            {%scripts%}
        </head>
        <body>
            <div class="container main">
                {%app_entry%}
            </div>
            {%config%}
            {%renderer%}
        </body>
    </html>
"""
