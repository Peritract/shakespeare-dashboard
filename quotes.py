import dash_html_components as html


def get_random_quotes(data, n):
    """
    Takes a Pandas dataframe and an integer, n;
    returns n randomly selected lines formatted as quotes in html
    """

    # Only pull quotes of more than 2 words
    quotes = data[data["tokens"].apply(len) > 2].sample(n)

    elements = []
    for i, row in enumerate(quotes.itertuples(), 1):
        elements.append(html.Div([html.Div(row.sentence),
                                 html.Div(row.speaker),
                                 html.Div(row.act),
                                 html.Div(row.scene)]))

    return html.Div(elements)
