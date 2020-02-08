from wordcloud import WordCloud  # Create wordclouds
import plotly.graph_objs as go  # Make it plotly-compatible
from sklearn.feature_extraction.text import CountVectorizer


def prepare_wordcloud_dict(col):
    """
    Takes a Pandas series of strings;
    returns a wordcloud-ready dictionary of terms & frequencies.
    """
    # Create a DTM

    vectorizer = CountVectorizer(max_features=10000, min_df=0.01,
                                 ngram_range=(1, 1))

    dtm = vectorizer.fit_transform(col)

    # Sum the frequencies of each term

    frequencies = dtm.sum(axis=0)

    # Create a dictionary of term frequencies

    freq_dict = {word: frequencies[0, id] for word, id in
                 vectorizer.vocabulary_.items()}

    # return the dict

    return freq_dict


def create_wordcloud(col):
    """
    Creates a wordcloud from a Pandas series as a plotly object
    """

    # Create a dict from the dataframe
    term_dict = prepare_wordcloud_dict(col)

    wc = WordCloud(width=800, height=300, colormap="Reds",
                   max_words=100)

    wc.generate_from_frequencies(term_dict)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x = []
    y = []
    for i in position_list:
        x.append(i[0])
        y.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    new_freq_list

    trace = go.Scatter(x=x, y=y,
                       textfont=dict(size=new_freq_list,
                                     color=color_list),
                       mode="text",
                       text=word_list)

    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False,
                                  'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False,
                                  'zeroline': False}})

    fig = go.Figure(data=[trace], layout=layout)

    return fig
