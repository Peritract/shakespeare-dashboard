from gutenberg.acquire import load_etext  # Import texts from Project Gutenberg
from gutenberg.cleanup import strip_headers  # Remove Project Gutenberg fluff

from parse_play_text import (separate_sentences,
                             remove_in_line_stage_directions,
                             create_play_data_frame)


def clean_macbeth(df):
    """
    Takes a dataframe of Macbeth text and performs specific cleaning/shaping.
    """

    # Filter out stage directions

    df = df[~((df["sentence"].str.contains("Stage_dir")) | (df["speaker"] ==
                                                            ""))]

    # Fix confusing character names

    df["speaker"] = df["speaker"].replace(r'[”"]\s', "", regex=True)

    # Collapse the witches together

    df["speaker"] = df["speaker"].replace(["First Witch",
                                           "Second Witch",
                                           "Third Witch"],
                                          "Witches")

    # Fix irritating inconsistencies

    df.replace("_Tiger", "Tiger", inplace=True)

    # Reset the index

    df.reset_index(inplace=True, drop=True)

    return df


def load_macbeth():
    """
    Sources Macbeth from Project Gutenberg, returns a cleaned dataframe
    of the play split by act, scene, speaker, and sentence.
    """
    raw_text = load_etext(1533)  # Collect the text
    raw_text = strip_headers(raw_text)  # Remove most metadata

    # Remove in-line stage directions

    raw_text = remove_in_line_stage_directions(raw_text)

    # Split the text into sentences

    sentences = separate_sentences(raw_text)

    # Remove introductory data, keeping only the text

    sentences = sentences[110:]

    # Create a dataframe from the sentences

    macbeth = create_play_data_frame(sentences)

    # Return the finished dataframe

    return clean_macbeth(macbeth)


def create_token_column(col):
    """
    Creates a cleaned and tokenised column
    based on a sentence column in a dataframe
    """
    return col
