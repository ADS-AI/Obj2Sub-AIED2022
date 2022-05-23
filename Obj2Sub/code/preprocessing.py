import re
import html

superscript_map = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "a": "ᵃ",
    "b": "ᵇ",
    "c": "ᶜ",
    "d": "ᵈ",
    "e": "ᵉ",
    "f": "ᶠ",
    "g": "ᵍ",
    "h": "ʰ",
    "i": "ᶦ",
    "j": "ʲ",
    "k": "ᵏ",
    "l": "ˡ",
    "m": "ᵐ",
    "n": "ⁿ",
    "o": "ᵒ",
    "p": "ᵖ",
    "q": "۹",
    "r": "ʳ",
    "s": "ˢ",
    "t": "ᵗ",
    "u": "ᵘ",
    "v": "ᵛ",
    "w": "ʷ",
    "x": "ˣ",
    "y": "ʸ",
    "z": "ᶻ",
    "A": "ᴬ",
    "B": "ᴮ",
    "C": "ᶜ",
    "D": "ᴰ",
    "E": "ᴱ",
    "F": "ᶠ",
    "G": "ᴳ",
    "H": "ᴴ",
    "I": "ᴵ",
    "J": "ᴶ",
    "K": "ᴷ",
    "L": "ᴸ",
    "M": "ᴹ",
    "N": "ᴺ",
    "O": "ᴼ",
    "P": "ᴾ",
    "Q": "Q",
    "R": "ᴿ",
    "S": "ˢ",
    "T": "ᵀ",
    "U": "ᵁ",
    "V": "ⱽ",
    "W": "ᵂ",
    "X": "ˣ",
    "Y": "ʸ",
    "Z": "ᶻ",
    "+": "⁺",
    "-": "⁻",
    "–": "⁻",
    "=": "⁼",
    "(": "⁽",
    ")": "⁾",
}
subscript_map = {
    "0": "₀",
    "1": "₁",
    "2": "₂",
    "3": "₃",
    "4": "₄",
    "5": "₅",
    "6": "₆",
    "7": "₇",
    "8": "₈",
    "9": "₉",
    "a": "ₐ",
    "b": "♭",
    "c": "꜀",
    "d": "ᑯ",
    "e": "ₑ",
    "f": "բ",
    "g": "₉",
    "h": "ₕ",
    "i": "ᵢ",
    "j": "ⱼ",
    "k": "ₖ",
    "l": "ₗ",
    "m": "ₘ",
    "n": "ₙ",
    "o": "ₒ",
    "p": "ₚ",
    "q": "૧",
    "r": "ᵣ",
    "s": "ₛ",
    "t": "ₜ",
    "u": "ᵤ",
    "v": "ᵥ",
    "w": "w",
    "x": "ₓ",
    "y": "ᵧ",
    "z": "₂",
    "A": "ₐ",
    "B": "₈",
    "C": "C",
    "D": "D",
    "E": "ₑ",
    "F": "բ",
    "G": "G",
    "H": "ₕ",
    "I": "ᵢ",
    "J": "ⱼ",
    "K": "ₖ",
    "L": "ₗ",
    "M": "ₘ",
    "N": "ₙ",
    "O": "ₒ",
    "P": "ₚ",
    "Q": "Q",
    "R": "ᵣ",
    "S": "ₛ",
    "T": "ₜ",
    "U": "ᵤ",
    "V": "ᵥ",
    "W": "w",
    "X": "ₓ",
    "Y": "ᵧ",
    "Z": "Z",
    "+": "₊",
    "-": "₋",
    "–": "₋",
    "=": "₌",
    "(": "₍",
    ")": "₎",
}


def convert_to_superscript(text):
    """
    Function that converts </sup> tag to superscript.
    Parameters
    ----------
    text: objective question

    Returns
    ----------
    text: converted question
    """
    SUP = str.maketrans(
        "".join(superscript_map.keys()), "".join(superscript_map.values())
    )
    return text.translate(SUP)


def convert_to_subscript(text):
    """
    Function that converts </sub> tag to subscript.
    Parameters
    ----------
    text: objective question

    Returns
    ----------
    text: converted question
    """
    SUB = str.maketrans("".join(subscript_map.keys()), "".join(subscript_map.values()))
    return text.translate(SUB)


def cleaning(text):
    """ "
    Function that Cleans the text. It handles the superscript and subscript
    tags, remove all the html tags.
    Parameters
    ----------
    text: objective question

    Returns
    -----------
    clean_text: clean form of objective question
    """
    org = text
    text = text.replace(":", "")
    text = html.unescape(text)
    text = text.replace("& # 39", "'")

    """Replacing sup tag with supercript"""
    n = len(text)
    ind = 0
    clean_text = ""

    while ind < len(text):
        if text[ind] == "<" and ind < n - 4 and text[ind + 1 : ind + 5] == "sup>":
            ind += 5  # sup> + 1
            temp = ""
            while ind + 5 < n:
                if text[ind] == "<" and text[ind + 1 : ind + 6] == "/sup>":
                    break
                temp += text[ind]
                ind += 1
            clean_text += convert_to_superscript(temp)
            ind += 6  # /sup> + 1

        else:
            clean_text += text[ind]
            ind += 1

    text = clean_text

    """Replacing sub tag with subcript"""
    ind = 0
    n = len(text)
    clean_text = ""

    while ind < len(text):
        if text[ind] == "<" and ind < n - 4 and text[ind + 1 : ind + 5] == "sub>":
            ind += 5  # sub> + 1
            temp = ""
            while ind + 5 < n:
                if text[ind] == "<" and text[ind + 1 : ind + 6] == "/sub>":
                    break
                temp += text[ind]
                ind += 1
            clean_text += convert_to_subscript(temp)
            ind += 6  # /sub> + 1
        else:
            clean_text += text[ind]
            ind += 1

    clean_text = re.sub("\\n", " ", clean_text)
    clean_text = re.sub("\\r", " ", clean_text)
    clean_text = re.sub("\\t", " ", clean_text)
    clean_text = re.sub("<[^>]*>", " ", clean_text)
    clean_text = clean_text.strip()
    clean_text = clean_text.strip(".")
    clean_text = clean_text.strip("-")
    clean_text = clean_text.replace(u"\xa0", u" ")

    return clean_text


def pre_process(text, flag_ques=False):
    """ "
    Function that preprocess the text, identify the category of the question
    Parameters
    ----------
    text: objective question

    Returns
    -----------
    process_text: pre-processed text
    int: category of the question
    """

    # Discarding the questions which contain tags like table, image, list, row tag
    text_ = str(text).lower()
    if "<table" in text_ or "<img" in text_ or "<li" in text_ or "<mrow" in text_:
        return "", -1

    text_ = cleaning(str(text))

    # Discarding the questions which are non-English
    flag_eng = False
    keyboard = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    for i in range(len(text_)):
        if text_[i].upper() in keyboard:
            flag_eng = True
    if not flag_eng:
        print("Not English")
        return "", -1

    # Identifying Category-3 Question
    category3 = [
        "not",
        "the following",
        "incorrect statement",
        "of the statements",
        "identify",
        "correct statement",
        "pick",
    ]
    for i in category3:
        if i in text_:
            return text_, 3

    # Identifying Category-1 Question
    whWords = [
        "Write",
        "Define",
        "What",
        "Where",
        "When",
        "Which",
        "Who",
        "Whom",
        "Why",
        "Whether",
        "How",
        "Did",
        "?",
    ]
    for i in whWords:
        if i in text_:
            return text_, 1

    # Identifying Category-4 Question
    if "_" in text_:
        return text_, 4

    # Identifying Category-2 Question
    if len(text_) > 0 and flag_ques:
        text_ = text_[0].lower() + text_[1:]
        return text_, 2
    elif len(text_) > 0:
        return text_, -1
    else:
        return "", -1
