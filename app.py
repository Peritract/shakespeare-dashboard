import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from source_plays import load_macbeth

from layouts import index_page, character_page, noPage

macbeth = load_macbeth()

app = app = dash.Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Shakespeare Dashboard</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Placeholder structure

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback to control the page layout

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """
    Return the appropriate page layout based on the url.
    """
    if pathname == '/':
        return index_page(macbeth)
    elif pathname == "/character":
        return character_page
    else:
        return noPage


# Run the server

if __name__ == '__main__':
    app.run_server(debug=True)
