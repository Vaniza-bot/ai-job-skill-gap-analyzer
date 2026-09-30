import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from flask import Flask, request
from flask_cors import CORS

from src.pipeline import analyze_job
from src.skill_gap import get_learning_recommendations

import pandas as pd
from sentence_transformers import SentenceTransformer


app = Flask(__name__)
CORS(app)


# Load skills
skills = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Natural Language Processing",
    "Transformers",
    "Hugging Face",
    "Large Language Models",
    "LLM",
    "RAG",
    "FAISS",
    "Docker",
    "Git",
    "GitHub",
    "Statistics",
    "Power BI",
    "Tableau",
    "FastAPI",
    "Flask",
    "Artificial Intelligence",
    "Computer Vision",
    "Data Science",
    "Generative AI",
    "SQL Server",
    "Keras",
    "Scipy"
]

skills_df = pd.DataFrame({
    "skill": skills
})


# Load semantic model once when server starts
model = SentenceTransformer("all-MiniLM-L6-v2")


@app.route("/")
def home():
    return {
        "message": "AI Job Skill Gap Analyzer API is running!"
    }


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    resume_text = data.get("resume")
    job_text = data.get("job_description")

    if not resume_text or not job_text:
        return {
            "error": "Resume and job_description are required."
        }, 400

    result = analyze_job(
        resume_text,
        job_text,
        skills_df,
        model
    )

    learning_recommendations = get_learning_recommendations(
        result["missing_skills"]
    )

    return {
        "skill_score": round(float(result["skill_score"]), 2),
        "tfidf_score": round(float(result["tfidf_score"]), 2),
        "semantic_score": round(float(result["semantic_score"]), 2),
        "hybrid_score": round(float(result["hybrid_score"]), 2),
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "learning_recommendations": learning_recommendations
    }


if __name__ == "__main__":
    app.run(debug=True)