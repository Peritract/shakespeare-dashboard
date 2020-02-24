import dash_core_components as dcc
import dash_html_components as html
from wordclouds import create_wordcloud
from quotes import get_random_quotes


def index_page(data):
    """
    Returns the html layout of the index page
    """
    main_index = [html.H1("INDEX"),
                  html.Div([html.A("Characters", href="/character"),
                           " | ", html.A("Search", href="/search")]),
                  dcc.Loading(html.Img(src=create_wordcloud(data["tokens"]))),
                  get_random_quotes(data, 5)]

    return main_index


# Character view

def character_page(data):
    """
    Returns the html layout of the character page
    """
    characters = list(data["speaker"].unique())
    character_page = [html.H1("CHARACTER"),
                      html.Div([html.A("Whole play", href="/"),
                                " | ", html.A("Search", href="/search")]),
                      dcc.Dropdown(id="character-dropdown",
                                   options=[{"label": i,
                                             "value": i} for i in characters],
                                   value="Macbeth",
                                   searchable=False,
                                   clearable=False),
                      dcc.Loading(html.Img(src=create_wordcloud(data["tokens"])))]
    return character_page


# 404 page

noPage = [html.H1("404"), html.Div("Page not found.")]
