import re
import nltk
import spacy
from helper import *
import pandas as pd
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download("punkt")
try:
    nltk.data.find('tag/averaged_perceptron_tagger')
except LookupError:
    nltk.download("averaged_perceptron_tagger")

try:
    nltk.data.find('corpus/reader/wordnet')
except LookupError:
    nltk.download("wordnet")
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

verbs = pd.read_csv("verbs.csv", sep="\t")


def name_questions(text):
    """Function for conversion of objective questions falling in
    "name" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """

    word_list = nltk.tokenize.word_tokenize(text)
    n = len(word_list)
    if word_list[0].lower() == "name" and word_list[1] == "the":
        out = "What is the name of the" + " " + " ".join(word_list[2:])
        return out
    elif word_list[0].lower() == "name" and word_list[1] == "of":
        out = "What is the name of the" + " " + " ".join(word_list[3:])
        return out
    else:
        return None


def on_questions(text, answer):
    
    nlp = spacy.load("en_core_web_sm")
    date_time_labels = ["DATE", "TIME"]
    place_labels = ["GPE", "LOC", "FAC", "EVENT"]
    doc = nlp(answer)
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
    word_list = nltk.tokenize.word_tokenize(text)
    ner_labels = []
    for ent in doc.ents:
        ner_labels.append(ent.label_)
    (past_verb_index, past_verb) = past_verb_check(pos_tagging(text))
    aux_verb = "does" if past_verb_index == None else "did"
    whWord = ""
    for label in date_time_labels:
        if label in ner_labels:
            whWord = "when"
            break
    for label in place_labels:
        if label in ner_labels:
            whWord = "where"
            break
    for index in range(len(word_list) - 1, -1, -1):
        if word_list[index] in auxilliary_verbs:
            aux_verb = word_list[index]
            word_list.pop(index)
            break
    if whWord == "":
        return None

    if past_verb != None and aux_verb == "did":
        word_list.pop(past_verb_index)
        word_list.insert(past_verb_index, past_verb)

    ind = seperator_finding(word_list)
    if ind != -1:
        out = (
            " ".join(word_list[: ind + 1])
            + " "
            + whWord
            + " "
            + aux_verb
            + " "
            + " ".join(word_list[ind + 1 : len(word_list) - 1])
        )
    else:
        out = (
            whWord + " " + aux_verb + " " + " ".join(word_list[0 : len(word_list) - 1])
        )
    return out


def as_for_questions(text):
    """Function for conversion of objective questions falling in
    "as/for" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """

    word_list = nltk.tokenize.word_tokenize(text)
    n = len(word_list)
    for i in range(n):
        word_list[i] = word_list[i].strip()
    out = ""
    arr = ["is", "are", "was", "known"]
    if n - 3 >= 0 and word_list[n - 3] == "also" and word_list[n - 2] == "known":
        ind = seperator_finding(word_list)
        if ind == -1:
            out = "What is another name of" + " " + " ".join(word_list[: n - 4])
        else:
            out = (
                " ".join(word_list[: ind + 1])
                + " "
                + "what is another name of"
                + " "
                + " ".join(word_list[ind + 1 : n - 4])
            )
        return out

    elif n - 3 >= 0 and word_list[n - 3] in arr and word_list[n - 2] == "known":
        ind = seperator_finding(word_list)
        if ind == -1:
            out = (
                "What"
                + " "
                + word_list[n - 3]
                + " "
                + " ".join(word_list[: n - 3])
                + " "
                + "called"
            )
        else:
            out = (
                " ".join(word_list[: ind + 1])
                + " "
                + "what"
                + " "
                + word_list[n - 3]
                + " "
                + " ".join(word_list[ind + 1 : n - 3])
                + " "
                + "called"
            )
        return out

    elif n - 2 >= 0 and check_verb(word_list[n - 2]):
        ind = seperator_finding(word_list)
        arr = ["is", "was", "are", "were"]
        aux = "does"
        if n - 3 >= 0 and word_list[n - 3] in arr:
            aux = word_list[n - 3]
            word_list[n - 3] = ""
        if n - 4 >= 0 and word_list[n - 4] in arr:
            aux = word_list[n - 4]
            word_list[n - 4] = ""
        if ind == -1:
            out = "What" + " " + aux + " " + " ".join(word_list[:])
        else:
            out = (
                " ".join(word_list[: ind + 1])
                + " "
                + "what"
                + " "
                + aux
                + " "
                + " ".join(word_list[ind + 1 :])
            )

    elif n - 2 >= 0 and check_verb(word_list[n - 2]) == False:
        aux = "does"
        ind = seperator_finding(word_list)
        if ind == -1:
            out = "What" + " " + aux + " " + " ".join(word_list[:])
        else:
            out = (
                " ".join(word_list[: ind + 1])
                + " "
                + "what"
                + " "
                + aux
                + " "
                + " ".join(word_list[ind + 1 :])
            )

    return out


def from_questions(text):
    """Function for conversion of objective questions falling in
    "from" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """

    word_list = nltk.tokenize.word_tokenize(text)
    n = len(word_list)
    ind = seperator_finding(word_list)
    if ind == -1:
        out = "From where" + " " + " ".join(word_list[: n - 1])
    else:
        out = (
            " ".join(word_list[: ind + 1])
            + " "
            + "from where"
            + " "
            + " ".join(word_list[ind + 1 : n - 1])
        )
    # print(out)
    return out


def because_questions(text):
    """Function for conversion of objective questions falling in
    "because" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """

    word_list = nltk.tokenize.word_tokenize(text)
    n = len(word_list)
    ind = seperator_finding(word_list)
    if ind == -1:
        out = "Why" + " " + " ".join(word_list[: n - 1])
    else:
        out = (
            " ".join(word_list[: ind + 1])
            + " "
            + "why"
            + " "
            + " ".join(word_list[ind + 1 : n - 1])
        )
    # print(out)
    return out


def called_questions(text):
    """Function for conversion of objective questions falling in
    "called" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """

    word_list = nltk.tokenize.word_tokenize(text)
    n = len(word_list)
    arr = ["is", "are", "was", "were"]

    if n - 2 >= 0 and word_list[n - 2] in arr:
        ind = seperator_finding(word_list)
        if ind == -1:
            out = (
                "What"
                + " "
                + word_list[n - 2]
                + " "
                + " ".join(word_list[: n - 2])
                + " "
                + " ".join(word_list[n - 1 :])
            )
        else:
            out = (
                " ".join(word_list[: ind + 1])
                + " "
                + "what"
                + " "
                + word_list[n - 2]
                + " "
                + " ".join(word_list[n - 1 :])
            )
        return out

    elif n - 3 >= 0 and word_list[n - 3] in arr:
        ind = seperator_finding(word_list)
        if ind == -1:
            out = (
                "What"
                + " "
                + word_list[n - 3]
                + " "
                + " ".join(word_list[: n - 3])
                + " "
                + " ".join(word_list[n - 2 :])
            )
        else:
            out = (
                " ".join(word_list[: ind + 1])
                + " "
                + "what"
                + " "
                + word_list[n - 3]
                + " "
                + " ".join(word_list[n - 2 :])
            )
        return out

    else:
        return None


def be_helper(text):
    """Helper Function for conversion of objective questions falling in
    "be" category. It is used to find a separator from end

    Return
    ----------
    index: the index of the separator
    """

    index = -1
    arr = ["would", "should", "will", "shall", "can"]
    endTokenIndex = len(text) - 1 if text[-1] == "." else len(text) - 2
    for i in range(endTokenIndex, -1, -1):
        if text[i] in arr:
            return i
    return index


def be_questions(text):
    """Function for conversion of objective questions falling in
    "be" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """

    word_list = nltk.tokenize.word_tokenize(text)
    ind = seperator_finding(word_list)
    aux_verb_ind = be_helper(word_list)

    n = len(word_list)

    if aux_verb_ind == -1:
        word_list.insert(n - 1, "would")
        word_list[n] = ""
        aux_verb_ind = n - 1
    if ind != -1:
        out = (
            " ".join(word_list[: ind + 1])
            + " "
            + "what"
            + " "
            + " ".join(word_list[aux_verb_ind:])
            + " "
            + " ".join(word_list[ind + 1 : aux_verb_ind])
        )
    else:
        out = (
            "What"
            + " "
            + " ".join(word_list[aux_verb_ind:])
            + " "
            + " ".join(word_list[:aux_verb_ind])
        )
    return out


def to_questions(text):
    word_list = nltk.tokenize.word_tokenize(text)
    whWord = "Why"
    out = None
    (past_verb_index, past_verb) = past_verb_check(pos_tagging(text))
    aux_verb = "does" if past_verb_index == None else "did"
    ind = seperator_finding(word_list)
    temp = 0 if ind == -1 else ind
    if word_list[-2].strip() == "due":
        if aux_verb_check(word_list[temp:]) != (None, None):
            (index, aux_verb) = aux_verb_check(word_list)
            if ind == -1:
                out = (
                    whWord
                    + " "
                    + aux_verb
                    + " "
                    + " ".join(word_list[:index])
                    + " "
                    + " ".join(word_list[index + 1 : -2])
                )
            else:
                out = (
                    " ".join(word_list[: ind + 1])
                    + " "
                    + whWord.lower()
                    + " "
                    + aux_verb
                    + " "
                    + " ".join(word_list[ind + 1 : index])
                    + " "
                    + " ".join(word_list[index + 1 : -2])
                )
        else:
            if aux_verb == "did":
                word_list.pop(past_verb_index)
                word_list.insert(past_verb_index, past_verb)
            if ind == -1:
                out = whWord + " " + aux_verb + " " + " ".join(word_list[:-2])
            else:
                out = (
                    " ".join(word_list[: ind + 1])
                    + " "
                    + whWord.lower()
                    + " "
                    + aux_verb
                    + " "
                    + " ".join(word_list[ind + 1 : -2])
                )

    return out


def at_questions(text):
    """Function for conversion of objective questions falling in
    "at" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """

    word_list = nltk.tokenize.word_tokenize(text)
    index = seperator_finding(word_list)
    if index == -1:
        question = "Where" + " " + " ".join(word_list[:-1])
    else:
        question = (
            " ".join(word_list[:index])
            + ", "
            + "where"
            + " "
            + " ".join(word_list[index + 1 : -1])
        )
    # print(question)
    return question


def means_questions(text):
    """Function for conversion of objective questions falling in
    "means" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """

    word_list = nltk.tokenize.word_tokenize(text)
    index = seperator_finding(word_list)
    if index == -1:
        question = "What does" + " " + " ".join(word_list[:])
    else:
        question = (
            " ".join(word_list[:index])
            + ", "
            + "what does"
            + " "
            + " ".join(word_list[index + 1 :])
        )
    return question


def year_questions(text):
    """Function for conversion of objective questions falling in
    "year" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """

    word_list = nltk.tokenize.word_tokenize(text)
    index = seperator_finding(word_list)
    question = None
    arr = ["in", "by"]
    c = 0
    for i in range(len(word_list) - 1, -1, -1):
        c += 1
        if word_list[i] in arr:
            if index == -1:
                question = (
                    word_list[i]
                    + " "
                    + "which"
                    + " "
                    + word_list[-1]
                    + " "
                    + " ".join(word_list[:-c])
                )
            else:
                question = (
                    " ".join(word_list[:index])
                    + ", "
                    + word_list[i]
                    + " "
                    + "which"
                    + " "
                    + word_list[-1]
                    + " "
                    + " ".join(word_list[index + 1 : -c])
                )
            break
    return question


def is_are_was_were_questions(text, lastWord):
    """Function for conversion of objective questions falling in
    "is/are/was/were" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """

    word_list = nltk.tokenize.word_tokenize(text)
    index = seperator_finding(word_list)
    if index == -1:
        question = "What" + " " + lastWord + " " + " ".join(word_list[:-1])
    else:
        question = (
            " ".join(word_list[:index])
            + ", "
            + "what"
            + " "
            + lastWord
            + " "
            + " ".join(word_list[index + 1 : -1])
        )
    return question


def the_questions(text,answer):
    """Function for conversion of objective questions falling in "the"
    category.

    Parameters
    -----------
    text: complete objective question after cleaning
    """

    from nltk.stem import WordNetLemmatizer

    lemmatizer = WordNetLemmatizer()
    word_list = nltk.tokenize.word_tokenize(text)
    last_word = text.split()[-1]
    second_last_word = text.split()[-2]
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
    whWord = "What"

    if (
        second_last_word == "in"
        or second_last_word == "inside"
        or second_last_word == "into"
    ):
        """Handling particular sub-category of questions having their second-last word as
        "in" or some similar words such as "inside" or "into"
        """
        nlp = spacy.load("en_core_web_sm")
        date_time_labels = ["DATE", "TIME"]
        place_labels = ["GPE", "LOC", "FAC", "EVENT"]
        doc = nlp(answer)

        ner_labels = []
        for ent in doc.ents:
            ner_labels.append(ent.label_)

        whWord = "Where"
        for label in date_time_labels:
            if label in ner_labels:
                whWord = "When"
                break
        
    elif second_last_word == "by":
        ques = by_questions(" ".join(word_list[:-1]))

    flag = 0
    index = seperator_finding(word_list)
    for verb in auxilliary_verbs:
        if verb in word_list:
            ind = word_list.index(verb)
            if index == -1:
                ques = (
                    whWord
                    + " "
                    + verb
                    + " "
                    + " ".join(word_list[0:ind])
                    + " "
                    + " ".join(word_list[ind + 1 : len(word_list) - 2])
                )
            else:
                ques = (
                    " ".join(word_list[0:index])
                    + whWord
                    + " "
                    + verb
                    + " "
                    + " ".join(word_list[index:ind])
                    + " "
                    + " ".join(word_list[ind + 1 : len(word_list) - 2])
                )
            flag = 1
            return ques
            # break
    if flag == 0:
        past_verb_forms = ["VBD", "VBN"]
        thirdPerson_verb_forms = ["VBZ"]
        check = 0
        # check2=0
        taggedList = pos_tagging(text)
        for tags in taggedList:
            if tags[1] in past_verb_forms:
                check = 1 - check
                new_word = lemmatizer.lemmatize(tags[0], pos="v")
                ind = word_list.index(tags[0])
                word_list.remove(tags[0])
                word_list.insert(ind, new_word)
                if index == -1:
                    ques = whWord + " " + "did" + " " + " ".join(word_list[0:-2])
                else:
                    ques = (
                        " ".join(word_list[0:index])
                        + " "
                        + whWord
                        + " "
                        + "did"
                        + " "
                        + " ".join(word_list[index:-2])
                    )
                return ques
        if check == 0:
            for tags in taggedList:
                if tags[1] in thirdPerson_verb_forms:
                    check = 1 - check
                    new_word = lemmatizer.lemmatize(tags[0], pos="v")
                    ind = word_list.index(tags[0])
                    word_list.remove(tags[0])
                    word_list.insert(ind, new_word)
                    if index == -1:
                        ques = whWord + " " + "does" + " " + " ".join(word_list[0:-2])
                    else:
                        ques = (
                            " ".join(word_list[0:index])
                            + " "
                            + whWord
                            + " "
                            + "does"
                            + " "
                            + " ".join(word_list[index:-2])
                        )
                    return ques
            if check == 0:

                if index == -1:
                    ques = whWord + " " + "does" + " " + " ".join(word_list[0:-2])
                else:
                    ques = (
                        " ".join(word_list[0:index])
                        + " "
                        + whWord
                        + " "
                        + "does"
                        + " "
                        + " ".join(word_list[index:-2])
                    )
                return ques


import pandas as pd


def by_helper(end, verb, start, Wh, flag=0):
    """Helper Function for conversion of objective questions falling in
    "by" category. It concatenates the subarrays of the Objective question

    Paramters
    ----------
    verb: Verb which will be concatenated in front
    end: String after b in the cleaned objective question
    start: Cleaned Objective question from starting index upto the last verb i.e. b
    Wh: Wh- word to be concatnated in front
    flag: Indicate the order of concatenation

    Return
    ----------
    out: Subjective Question
    """
    try:
        verb = [verb[0].values[0]]
    except:
        verb = verb

    ind = seperator_finding(start)
    if ind != -1 and flag == 0:
        verb += start[ind + 1 :]
        start = start[:ind]
        out = " ".join(start) + " " + Wh.lower() + " " + " ".join(verb + end)

    elif ind != -1 and flag == 1:
        verb = start[ind + 1 :] + verb
        start = start[:ind]
        out = verb + end + start
        out = Wh + " " + " ".join(out)
    else:
        out = verb + end + start
        out = Wh + " " + " ".join(out)

    return out


def by_questions(text):
    """Function for conversion of objective questions falling in
    "by" category.

    Paramters
    ----------
    text: complete objective question after cleaning
    """
    word_list = nltk.tokenize.word_tokenize(text)
    n = len(word_list)
    for i in range(n):
        word_list[i] = word_list[i].strip()

    # Removing the string "by" from end
    if word_list[-1] == "by":
        word_list = word_list[:-1]
        n = len(word_list)

    # Renaming the columns of csv file
    col = [
        "present_simple_1st",
        "present_simple_3rd",
        "past_simple",
        "past_participle",
        "present_participle",
    ]
    verbs.columns = col

    # Searching for the verb from end
    for i in range(n - 1, -1, -1):

        question = ""
        flag = False
        temp = ""
        index = -1
        for j in range(4):
            if (verbs[col[j]] == word_list[i]).any():
                temp = col[j]
                index = j
                flag = True
                break

        if flag == True:

            # Found a verb

            if (
                word_list[i - 1] == "is"
                or word_list[i - 1] == "are"
                or word_list[i - 1] == "am"
            ):

                v = word_list[i]
                if index == 2:  # past_simple
                    v = verbs[verbs[temp] == word_list[i]].present_simple_3rd
                    question = by_helper([""], [""], word_list, "How")

                if index == 3:  # past_participle
                    v = verbs[verbs[temp] == word_list[i]].past_simple
                    question = by_helper(
                        word_list[i + 1 :], [v], word_list[: i - 1], "Who"
                    )

            elif word_list[i - 1] == "was" or word_list[i - 1] == "were":

                v = verbs[verbs[temp] == word_list[i]].past_simple
                question = by_helper(word_list[i + 1 :], [v], word_list[: i - 1], "Who")

            elif word_list[i - 1] == "be":

                v = verbs[verbs[temp] == word_list[i]].present_simple_1st
                question = by_helper([""], [""], word_list, "How")

            elif word_list[i - 1] == "being" and (
                word_list[i - 2] == "is"
                or word_list[i - 2] == "are"
                or word_list[i - 2] == "am"
            ):

                v = (
                    word_list[i - 2]
                    + " "
                    + verbs[verbs[temp] == word_list[i]].present_participle
                )
                question = by_helper([""], [""], word_list, "How")

            elif word_list[i - 1] == "been" and (
                word_list[i - 2] == "has" or word_list[i - 2] == "have"
            ):

                v = word_list[i - 2] + " " + word_list[i]
                question = by_helper(
                    word_list[i + 1 :], [v], word_list[: i - 2], "How", 1
                )

            else:
                question = "How" + " ".join(word_list[:-1])
            try:
                question = question.values[0].replace(".", "")
            except:
                question = question.replace(".", "")

            question = nltk.tokenize.word_tokenize(question)
            n = len(question)
            for i in range(n):
                question[i] = question[i].strip()
            question = " ".join(question)
            return question


def compute(x, y):

    notWh = []
    notWh.append(x)
    notWh_ans = []
    notWh_ans.append(y)
    converted_ques = ""
    for i in range(len(notWh)):

        flag = 0

        last_word = x.split(" ")[-1]
        last_word = re.sub(r"[^\w\s]", "", last_word)
        last_word = re.sub(r"[ \t]", "", last_word)
        last_word = last_word.lower()

        first_word = x.split(" ")[0]
        first_word = first_word.lower()

        notWh[i] = x[0].lower() + x[1:]

        temp = []
        text = notWh[i]
        answer = notWh_ans[i]
        in_synonym_words = ["in", "inside", "into"]
        commonCategories = ["is", "are", "was", "were"]
        """Capturing "a" cateogry"""
        if last_word == "a" or last_word == "a/an":
            text = notWh[i]
            word_list = nltk.tokenize.word_tokenize(text)
            n = len(word_list)
            if n - 2 >= 0:
                last_word = word_list[-2]
                text = " ".join(word_list[: n - 1])

            """Capturing "in/inside/into" cateogries"""
        if last_word in in_synonym_words:
            text = text + " " + "the"
            temp.append(the_questions(text,answer))

            """Capturing "the" cateogries"""
        if last_word.lower() == "the":
            temp.append(the_questions(text,answer))

            """Capturing "name" cateogry"""
        if first_word.lower() == "name":
            temp.append(name_questions(text))

            """Capturing "be" cateogry"""
        if last_word == "be":
            temp.append(be_questions(text))

            """Capturing "called" cateogry"""
        if last_word == "called":
            temp.append(called_questions(text))

            """Capturing "because" cateogry"""
        if last_word == "because":
            temp.append(because_questions(text))

            """Capturing "from" cateogry"""
        if last_word == "from":
            temp.append(from_questions(text))

            """Capturing "as/for" cateogry"""
        if last_word == "for" or last_word == "as":
            temp.append(as_for_questions(text))

            """Capturing "to" cateogry"""
        if last_word == "to":
            temp.append(to_questions(text))

            """Capturing "on" category"""
        if last_word == "on":
            temp.append(on_questions(text, notWh_ans[i]))

            """Capturing "is/are/was/were" categories"""
        if last_word in commonCategories:
            last_word_index = commonCategories.index(last_word)
            last_word = commonCategories[last_word_index]
            temp.append(is_are_was_were_questions(text, last_word))

            """Capturing "by" category"""
        if last_word == "by":
            temp.append(by_questions(text))

            """Capturing "means" cateogry"""
        if last_word == "means":
            temp.append(means_questions(text))

            """Capturing "year" cateogry"""
        if last_word == "year":
            temp.append(year_questions(text))

            """Capturing "at" cateogry"""
        if last_word == "at":
            temp.append(at_questions(text))

        if len(temp) > 0 and temp[0] is not None:
            converted_ques = temp[0] + "?"

    return converted_ques
