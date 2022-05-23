import nltk
from nltk.stem import WordNetLemmatizer


def check_verb(text):
    """ "
    Function that checks the form of the verb
    Parameters
    ----------
    text: objective question

    Returns
    -----------

    """
    wordsList = nltk.word_tokenize(text)
    Verbs = ["VB", "VBZ", "VBD", "VBN", "VBG", "VBP"]
    tagged = nltk.pos_tag(wordsList)
    return tagged[0][1] in Verbs


def pos_tagging(text):
    """ "
    Function that compute the POS tags of the input text
    Parameters
    ----------
    text: objective question

    Returns
    -----------
    tagged: array of pos tags
    """

    tokenized = nltk.tokenize.sent_tokenize(text)
    tagged = []
    for i in tokenized:
        wordsList = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(wordsList)

    return tagged


def aux_verb_check(wordList):
    """ "
    Function that checks auxilary verbs in the input list of words
    Parameters
    ----------
    wordList: list of words

    Returns
    -----------
    """
    auxilliary_verbs = [
        "is",
        "are",
        "was",
        "were",
        "has",
        "have",
        "can",
        "should",
        "do",
        "would",
        "will",
        "does",
    ]
    for verb in auxilliary_verbs:
        for word in wordList:
            if word == verb:
                return wordList.index(word), verb
    return None, None


def seperator_finding(word_tokens):
    """
    Function for finding an in between comma or full-stop in an objective question.
    The first part of the question is often used for description.
    Parameters
    ----------
    word_tokens: word_tokenized list of an objective question

    Returns
    --------
    index: index of a found seperator, by default -1
    """

    index = -1
    endTokenIndex = (
        len(word_tokens) - 1 if word_tokens[-1] == "." else len(word_tokens) - 2
    )
    for i in range(endTokenIndex, -1, -1):
        if word_tokens[i] == "," or word_tokens[i] == ".":
            return i
    return index


def past_verb_check(taggedList):
    """ "
    Function that lemmatizes the list of words
    ----------
    wordList: list of words

    Returns
    -----------
    """
    lemmatizer = WordNetLemmatizer()
    past_verb_forms = ["VBD", "VBN"]
    for index, tags in enumerate(taggedList):
        if tags[1] in past_verb_forms:
            return index, lemmatizer.lemmatize(tags[0], pos="v")
    return None, None
