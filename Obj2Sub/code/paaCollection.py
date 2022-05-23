import people_also_ask


def fetch_paa(ques, ans):
    """
    Function collects PAA Questions from Google
    """
    questions = []
    combinations = [ques + " " + ans, ans + " " + ques, ques, ques + " " + "what"]
    for c in combinations:
        questions.extend(people_also_ask.get_related_questions(c)[:4])
    questions = list(set(questions))
    return questions
