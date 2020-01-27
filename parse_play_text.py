import re  # Regular expressions

from pandas import DataFrame  # Data manipulation


def mark_line_for_separation(line):
    """
    Tag stage directions, acts, and scenes.
    """
    if line[0] == " ":
        if line[-1] != ".":
            return "Stage_dir" + line + "."
        else:
            return "Stage_dir" + line
    elif "ACT " in line or "SCENE " in line:
        return line + "."
    return line


def remove_in_line_stage_directions(play_string):
    """
    Remove in-line stage directions contained in square brackets.
    """
    return re.sub(r"\[[\S\s]+?\]", "", play_string)


def separate_sentences(play_string):
    """
    Separate sentences in the play_string,
    returning a list of sentences.
    """

    lines = play_string.split("\n")  # First split by lines

    # Remove lines with no content

    lines = list(filter(lambda x: len(x) > 0, lines))

    # Tag inline stage directions and act/scene markers

    lines = [mark_line_for_separation(line) for line in lines]

    # Join all the marked text back together again

    raw_text = "\n".join(lines)

    # Remove redundant new lines

    sentences = re.sub("\n{2,}", " ", raw_text)

    # Remove repeated spaces

    sentences = re.sub(r"\s+", " ", sentences)

    # Tag sentences for splitting, preserving punctuation

    sentences = re.sub("([.?!])", r"\1SPLIT_ME", sentences)

    # Split text into sentences

    sentences = re.split("SPLIT_ME", sentences)

    return sentences


def parse_play_sentences(sentences):
    """
    Return sentences from the play tagged with act, scene, and speaker.
    """

    act = 0
    scene = 0
    speaker = ""
    parsed_sentences = []

    for sentence in sentences:
        if "ACT" in sentence:
            act += 1
        if "SCENE" in sentence:
            scene += 1
            speaker = ""
        elif sentence.upper() == sentence:
            speaker = sentence.strip()[:-1].title()
        elif "STG_DIR" not in sentence:
            parsed_sentences.append((act, scene, speaker, sentence.strip()))

    return parsed_sentences


def create_play_data_frame(sentences):
    """
    Creates a dataframe of act, scene, speaker, and sentence
    from a list of all sentences in a play.
    """

    # Tag sentences with key information

    sentences = parse_play_sentences(sentences)

    # Construct the dataframe

    df = DataFrame(columns=["act", "scene", "speaker", "sentence"],
                   data=sentences)

    return df
