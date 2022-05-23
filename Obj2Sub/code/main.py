import pandas as pd
import html
import nltk
import pickle
import math
from nltk.tokenize import sent_tokenize, word_tokenize
from preprocessing import *
from clusteringMethod import *
from paaMethod import *
from transformer import *


max_perplexity = 50000
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download("punkt")



def run(ques, ans):
    global max_perplexity
    ques, cq = pre_process(ques, True)
    ans, ca = pre_process(ans)
    # Converted question of Category-1
    if cq == 1:
        return [ques, ans, ques, 1]

    # Converted question of Category-2
    if cq == 2:
        converted_ques = compute(ques, ans)
        if converted_ques != "":
            perplexity = get_perplexity(converted_ques)
            confidence = 0
            if perplexity < max_perplexity:
                confidence = 1 - (perplexity / max_perplexity)
            return [ques, ans, converted_ques, confidence]
        else:
            T5_ = get_T5(ques, ans)

            lst = get_paaQuestions(ques, ans) + T5_
            lst = T5_
            if len(lst) > 0:
                res = sorted(lst, key=lambda x: -x[1])
                temp = [ques, ans]
                for i in range(len(res)):
                    temp.append(res[i][0].strip())
                    temp.append(str(float(res[i][1][0][0])))
                return temp

    return [ques, ans, "Unable to resolve", 0]


def file_convert(file_input):
    global max_perplexity
    df = pd.read_csv(file_input, header=None)
    out_df = []
    for i in range(len(df)):
        temp = []
        ques = df.iloc[i, 0]
        ans = df.iloc[i, 1]
        temp = run(ques, ans)
        temp = [ques, ans] + temp
        out_df.append(temp)

    out = pd.DataFrame(
        out_df,
        columns=[
            "Original Ques",
            "Original Answer",
            "Cleaned Objective Ques",
            "Cleaned Answer",
            "Subjective Ques #1",
            "confidence #1",
            "Subjective Ques #2",
            "confidence #2",
            "Subjective Ques #3",
            "confidence #3",
        ],
    )
    return out

while True:
    ques = input("Ques: ").strip(" ")
    ans = input("Ans: ").strip(" ")
    print("Converted Question: ", run(ques, ans)[2])
