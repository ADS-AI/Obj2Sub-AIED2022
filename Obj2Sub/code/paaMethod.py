import re
import nltk
import spacy
import pickle
from score import *
from paaCollection import *
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize


stop_words = set(stopwords.words("english"))
nlp = spacy.load("en_core_web_sm")
ps = PorterStemmer()

file = open("Give_Questions.p",'rb')
d = pickle.load(file)

aux_verbs = ["is","are","was","were","do","does","have","has","will","shall","would","should","had","be"]

def removeStopwords(text):
    """
    Function that removes all the stopwords.
    Parameters
    ----------
    text: objective question

    Returns
    ----------
    text_: converted question
    """
    words = word_tokenize(str(text).lower())
    text_ = " ".join(str(j) for j in words if j not in stop_words and (len(j) != 1))
    return text_


def get_tags(text):
    doc = nlp(text)
    tags = []
    words = []
    for t in doc:
        tags.append(t.pos_)
        words.append(str(t))
    return tags, words


def checkPhrases(text,paa_ques):
    """
    Function that checks if text has some important
    phrases which are not covered paa_ques
    """
    paa_ques = re.sub(r"[^\w\s]", "", paa_ques)
    text = re.sub(r"[^\w\s]", "", text)

    check_set = set()

    verbs = ["VBD", "VBG", "VBZ", "VBP", "VBN", "VB"]
    tags, words = get_tags(paa_ques)
    tags2, words2 = get_tags(text)

    for ind, word in enumerate(words2):
        if word.strip() in stop_words or tags2[ind] == "VERB" or tags2[ind] in verbs:
            continue
        else:
            check_set.add(word.lower())
    for j in range(len(words)):
        words[j] = ps.stem(words[j])

    for word in check_set:
        if ps.stem(word) not in words:
            return True
    if paa_ques.split()[0].lower() in aux_verbs:
        return True
    return False


def checkWh(text):
    """
    Function that checks that input text should have
    atmost one wh-word.
    """
    whWord = ["what", "which", "when", "where", "how", "why", "whether"]
    text = word_tokenize(text.lower())
    count_ = 0
    for iter in text:
        if iter.strip() in whWord:
            count_ += 1
    text = removeStopwords(text) + " "
    for key in d:
        key = " " + removeStopwords(key) + " "
        if key.lower() in text.lower():
            print(key)
            count_ += 1
    if count_ > 1:
        return False
    return True


def removeSuffix(text):
    """
    Function that removes unwanted words from the suffix of the text.
    """
    reg = re.compile(r"\bclass [0-9][0-2]?\b", re.IGNORECASE)
    reg_ = re.compile(r"\bchapter [0-9]?[0-2]?\b", re.IGNORECASE)
    r_words = ["Quizlet", "Answer", "quizlet", "answer"]

    phrases = reg.findall(text)
    for p in phrases:
        text = text.replace(p, "")

    phrases = reg_.findall(text)
    for p in phrases:
        text = text.replace(p, "")

    for p in r_words:
        text = text.replace(p, "")
    return text


def get_paaQuestions(ques, ans):
	"""
	Function returns top 3 PAA questions
	"""
	text = ques + " " + ans
	questions = fetch_paa(ques, ans)
	# print(questions)
	candidates = []
	candidates_score = []
	for q in questions:
		if(checkWh(q) and checkPhrases(text,q)):
			if(q.split(" ")[0].lower() == "why"):
				text_ = text.replace("than", "")
				tags,words = get_tags(text_)
				if ("SCONJ"  in tags) or ("due"  in words) or ("to"  in words):
					curr_score = get_score(text, q)
					candidates.append(q)
					candidates_score.append(curr_score)
			else:
				curr_score = get_score(text, q)
				candidates.append(q)
				candidates_score.append(curr_score)
	zipped = zip(candidates, candidates_score)
	res = sorted(zipped, key = lambda x: -x[1])
	return res[:3]





            


