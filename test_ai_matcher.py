from matcher import calculate_match_score

resume = """
Experienced Python developer.
Worked on machine learning and deep learning projects.
"""

job = """
Looking for AI engineer with machine learning experience.
"""

print(
    calculate_match_score(
        resume,
        job
    )
)