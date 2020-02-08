import dash_core_components as dcc
import dash_html_components as html
import dash_table as table
from wordclouds import create_wordcloud


def index_page(data):
    """Returns the html layout of the index page
    """

    main_index = [html.H1("INDEX"), dcc.Graph(
            id='wordcloud-figure',
            figure=create_wordcloud(data["tokens"]))]

    return main_index


# Character view

character_page = html.H1("CHARACTER")

# 404 page

noPage = [html.H1("404"), html.Div("Page not found.")]
