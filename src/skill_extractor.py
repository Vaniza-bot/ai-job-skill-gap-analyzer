def extract_skills(text, skills_df):
    text = text.lower()
    found_skills = []

    for skill in skills_df["skill"]:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def calculate_skill_match(resume_skills, job_skills):
    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)

    matched = resume_set.intersection(job_set)
    missing = job_set - resume_set

    if len(job_set) == 0:
        score = 0
    else:
        score = (len(matched) / len(job_set)) * 100

    return score, list(matched), list(missing)