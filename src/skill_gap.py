from collections import Counter
import pandas as pd


learning_map = {
    "deep learning": "Deep Learning with PyTorch",
    "statistics": "Statistics for Data Science",
    "tensorflow": "TensorFlow and Deep Learning",
    "power bi": "Power BI for Data Analysis",
    "large language models": "Large Language Models (LLMs)",
    "rag": "Retrieval-Augmented Generation (RAG)",
    "llm": "Large Language Models (LLMs)",
    "scikit-learn": "Scikit-learn for Machine Learning",
    "artificial intelligence": "Artificial Intelligence Fundamentals",
    "tableau": "Tableau for Data Visualization",
    "fastapi": "FastAPI for Python APIs",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "flask": "Flask Web Development",
    "computer vision": "Computer Vision",
    "faiss": "FAISS and Vector Databases"
}


def analyze_skill_gaps(results_df):
    all_missing_skills = []

    for skills in results_df["missing_skills"]:
        all_missing_skills.extend(skills)

    skill_counts = Counter(all_missing_skills)

    skill_gap_df = (
        pd.DataFrame(
            skill_counts.items(),
            columns=["skill", "job_count"]
        )
        .sort_values("job_count", ascending=False)
        .reset_index(drop=True)
    )

    return skill_gap_df


def get_priority(count):
    if count >= 3:
        return "High"
    elif count == 2:
        return "Medium"
    else:
        return "Low"


def get_learning_recommendations(missing_skills):
    recommendations = []

    for skill in missing_skills:
        skill_lower = skill.lower()

        recommendation = learning_map.get(
            skill_lower,
            f"Learn {skill}"
        )

        if skill_lower in ["deep learning", "statistics", "tensorflow"]:
            priority = "High"
        elif skill_lower in ["power bi", "scikit-learn", "rag", "large language models", "llm"]:
            priority = "Medium"
        else:
            priority = "Low"

        recommendations.append({
            "skill": skill,
            "recommendation": recommendation,
            "priority": priority
        })

    return recommendations