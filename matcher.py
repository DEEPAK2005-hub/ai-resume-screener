import re

def calculate_match_score(resume_text, job_description):

    resume_words = set(re.findall(r'\w+', resume_text.lower()))
    jd_words = set(re.findall(r'\w+', job_description.lower()))

    if len(jd_words) == 0:
        return 0

    matched_words = resume_words.intersection(jd_words)

    score = (len(matched_words) / len(jd_words)) * 100

    return round(score, 2)