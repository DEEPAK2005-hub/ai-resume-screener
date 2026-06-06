SKILLS = [
    "python",
    "sql",
    "machine learning",
    "pandas",
    "numpy",
    "scikit-learn",
    "streamlit",
    "tensorflow",
    "git",
    "github"
]

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills