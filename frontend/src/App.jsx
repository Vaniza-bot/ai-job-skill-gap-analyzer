import { useState } from "react";
import "./App.css";

function App() {
  const [resume, setResume] = useState("");
  const [jobDescription, setJobDescription] = useState("");

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeJob = async () => {
    if (!resume.trim() || !jobDescription.trim()) {
      setError("Please enter both your resume and the job description.");
      return;
    }

    setLoading(true);
    setError("");
    setResults(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resume: resume,
          job_description: jobDescription,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
      }

      setResults(data);
    } catch (error) {
      setError(
        "Could not connect to the AI backend. Make sure Flask is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>AI Job Skill Gap Analyzer</h1>
        <p>
          Analyze your resume against a job description and discover
          your skill gaps.
        </p>
      </header>

      <main className="container">
        <section className="input-section">
          <div className="input-card">
            <h2>Your Resume</h2>
            <p>Paste your resume text below.</p>

            <textarea
              value={resume}
              onChange={(e) => setResume(e.target.value)}
              placeholder="Paste your resume here..."
            />
          </div>

          <div className="input-card">
            <h2>Job Description</h2>
            <p>Paste the job description you want to analyze.</p>

            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
            />
          </div>
        </section>

        {error && <p className="error-message">{error}</p>}

        <button
          className="analyze-button"
          onClick={analyzeJob}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Job Match"}
        </button>

        {results && (
          <section className="results-section">
            <h2>Analysis Results</h2>

            <div className="score-grid">
              <div className="result-card">
                <h3>Hybrid Score</h3>
                <strong>{results.hybrid_score}%</strong>
              </div>

              <div className="result-card">
                <h3>Skill Match</h3>
                <strong>{results.skill_score}%</strong>
              </div>

              <div className="result-card">
                <h3>Semantic Score</h3>
                <strong>{results.semantic_score}%</strong>
              </div>

              <div className="result-card">
                <h3>TF-IDF Score</h3>
                <strong>{results.tfidf_score}%</strong>
              </div>
            </div>

            <div className="skills-container">
              <div className="skills-card">
                <h3>Matched Skills</h3>

                <div className="skill-list">
                  {results.matched_skills.map((skill, index) => (
                    <span className="matched-skill" key={index}>
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div className="skills-card">
                <h3>Missing Skills</h3>

                <div className="skill-list">
                  {results.missing_skills.map((skill, index) => (
                    <span className="missing-skill" key={index}>
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="recommendations-card">
              <h3>Learning Recommendations</h3>

              {results.learning_recommendations.map((item, index) => (
                <div className="recommendation" key={index}>
                  <div>
                    <strong>{item.skill}</strong>
                    <p>{item.recommendation}</p>
                  </div>

                  <span className={`priority ${item.priority.toLowerCase()}`}>
                    {item.priority}
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;