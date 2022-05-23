from transformers import T5ForConditionalGeneration, T5Tokenizer
from score import *
import warnings
warnings.filterwarnings("ignore")
import re

# Add the absolute path to the downloaded folder as the attribute in below line.
question_model = T5ForConditionalGeneration.from_pretrained("Absolute Path to the T5_Squad_V1_Model")

question_tokenizer = T5Tokenizer.from_pretrained("t5-base")


def get_question(sentence, answer):
    text = "context: {} answer: {} </s>".format(sentence, answer)
    max_len = 256
    encoding = question_tokenizer.encode_plus(
        text, max_length=max_len, pad_to_max_length=True, return_tensors="pt"
    )

    input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

    outs = question_model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        early_stopping=True,
        num_beams=5,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        max_length=200,
    )

    dec = [question_tokenizer.decode(ids) for ids in outs]
    for i in range(len(dec)):
        dec[i] = dec[i].replace("question:", "")
        dec[i] = dec[i].strip()

    return dec


def get_T5(sent, answer):
    sentence_for_T5 = " ".join(sent.split())
    ques = get_question(sentence_for_T5, answer)
    out = []
    for q in ques:
        q = re.sub("<[^>]*>", " ", q)
        score = get_score(sent + " " + answer, q)
        out.append([q,score])
    return out
