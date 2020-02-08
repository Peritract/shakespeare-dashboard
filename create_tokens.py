
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from collections import defaultdict


def get_lemma(word, tag_dict, lemmatiser):
    """Gets the POS tag for a word, and then returns the lemmatized form of the word"""
    tag = pos_tag([word])[0][1][0]
    tag = tag_dict[tag]

    return lemmatiser.lemmatize(word, tag)


def lemmatise(col):
    """
    Takes a Pandas series containing token lists;
    returns the lemmatised form of the tokens.
    """
    # Lemmatisation dictionary

    tag_dict = defaultdict(lambda: wordnet.NOUN)
    tag_dict['J'] = wordnet.ADJ
    tag_dict['V'] = wordnet.VERB
    tag_dict['R'] = wordnet.ADV

    # Lemmatisation object

    lemma = WordNetLemmatizer()

    # Actually lemmatise the column
    col = col.apply(lambda x: [get_lemma(word, tag_dict, lemma) for word in x])

    # Return the column

    return col

def remove_simple(col):
    """
    Takes a Pandas series of lists of tokens;
    returns the series with stopwords and overly common words removed
    """
    # Remove common words

    stop_words = stopwords.words("english")
    stop_words.extend(["thou", "thee", "thy", "hath"])

    # Filter the words, removing stopwords and short (<= 2 letters) words
    col = col.apply(lambda x: [y for y in x if y not in stop_words
                               and len(y) > 2])

    return col


def create_token_column(col):
    """
    Creates a cleaned and tokenised column
    based on a sentence column in a dataframe
    """

    # Convert it to lowercase

    col = col.str.lower()

    # Remove all non-alphanumeric characters

    col = col.replace(r"\W", " ", regex=True)

    # Collapse repeated spaces

    col = col.replace(r"\s{2,}", " ", regex=True).str.strip()

    # Split the strings into tokens

    col = col.apply(word_tokenize)

    # Lemmatise the column

    col = lemmatise(col)

    # Remove boring words

    col = remove_simple(col)

    # Rejoin the token lists into strings

    col = col.apply(lambda x: " ".join(x))

    # Return the final, cleaned version

    return col