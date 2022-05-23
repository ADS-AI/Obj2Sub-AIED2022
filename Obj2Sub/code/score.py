import nltk
import math
import pickle
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("msmarco-distilroberta-base-v2")
max_perplexity = 50000

with open("TrainingCounts", "rb") as f:
    dict = pickle.load(f)
    trigram_counts = dict["Trigram"]
    bigram_counts = dict["Bigram"]
    vocab = dict["vocab"]
    f.close()


def get_perplexity(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    words = []
    for sentence in sentences:
        words.extend(nltk.word_tokenize(sentence))
    for word in words:
        vocab.add(word)
    temp = 1
    for ind, word in enumerate(words):
        if ind == 0:
            t = 0
            b = 0
            if ("\s", "\s", word) in trigram_counts:
                t = trigram_counts[("\s", "\s", word)]
            if ("\s", word) in bigram_counts:
                b = bigram_counts[("\s", word)]
            prob = (t + 1) / (b + len(vocab))
            temp *= 1 / prob

        elif ind == 1:
            t = 0
            b = 0
            if ("\s", words[ind - 1], word) in trigram_counts:
                t = trigram_counts[("\s", words[ind - 1], word)]
            if (words[ind - 1], word) in bigram_counts:
                b = bigram_counts[(words[ind - 1], word)]
            prob = (t + 1) / (b + len(vocab))
            temp *= 1 / prob

        elif ind > 1:
            t = 0
            b = 0
            if (words[ind - 2], words[ind - 1], word) in trigram_counts:
                t = trigram_counts[(words[ind - 2], words[ind - 1], word)]
            if (words[ind - 1], word) in bigram_counts:
                b = bigram_counts[(words[ind - 1], word)]
            prob = (t + 1) / (b + len(vocab))
            temp = temp / prob

    return math.pow(temp, 1 / len(words))


def get_score(text, ques):
    passage_embedding = model.encode(text)
    query_embedding = model.encode(ques)
    curr_score = util.pytorch_cos_sim(query_embedding, passage_embedding)
    return curr_score
