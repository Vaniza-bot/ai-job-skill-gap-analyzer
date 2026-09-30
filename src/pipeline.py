from .skill_extractor import extract_skills
from .job_matcher import match_job
from .text_matcher import calculate_tfidf_similarity
from .semantic_matcher import calculate_semantic_similarity


def analyze_job(resume_text, job_text, skills_df, model):
    # Extract skills
    resume_skills = extract_skills(resume_text, skills_df)
    job_skills = extract_skills(job_text, skills_df)

    # Skill matching
    skill_score, matched_skills, missing_skills = match_job(
        resume_skills,
        job_skills
    )

    # TF-IDF similarity
    tfidf_score = calculate_tfidf_similarity(
        resume_text,
        job_text
    )

    # Semantic similarity
    semantic_score = calculate_semantic_similarity(
        resume_text,
        job_text,
        model
    )

    # Hybrid score
    hybrid_score = (
        0.40 * skill_score
        + 0.20 * (tfidf_score)
        + 0.40 * semantic_score
    )

    return {
        "skill_score": skill_score,
        "tfidf_score": tfidf_score,
        "semantic_score": semantic_score,
        "hybrid_score": hybrid_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }