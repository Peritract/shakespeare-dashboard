from wordcloud import WordCloud  # Create wordclouds
from sklearn.feature_extraction.text import CountVectorizer  # Create DTMs
import io  # Write to a buffer, not a file
import base64  # Encode data as a uri


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

    # Generate a wordcloud

    wc = WordCloud(colormap="Reds", max_words=100)

    wc.generate_from_frequencies(term_dict)

    # Write the cloud to the buffer as an image

    image = wc.to_image()

    byte_io = io.BytesIO()

    image.save(byte_io, 'PNG')

    # Pull the image out of the buffer and encode it as a data_uri

    byte_io.seek(0)

    data_uri = base64.b64encode(byte_io.getvalue()).decode('utf-8').replace('\n', '')

    # Create a data string that can be passed to an html object

    src = 'data:image/png;base64,{0}'.format(data_uri)

    # Return the source string

    return src
