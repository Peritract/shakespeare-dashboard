import dash
import dash_core_components as dcc
import dash_html_components as html

from source_plays import load_macbeth

macbeth = load_macbeth()

app = app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1("Macbeth"),
                                html.P("macbeth")])

if __name__ == '__main__':
    app.run_server(debug=True)
