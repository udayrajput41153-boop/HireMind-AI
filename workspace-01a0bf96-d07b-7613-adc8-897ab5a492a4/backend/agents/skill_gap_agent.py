"""
AGENT 4 — Skill Gap Agent
Compares matched vs missing skills and turns misses into actionable gaps:
critical gaps (must-haves), stretch gaps (nice-to-haves), adjacent strengths
the candidate could build on, and concrete upskilling recommendations.
"""

LEARNING_HINTS = {
    "kubernetes": "Docker → Kubernetes path; build one deployment on EKS/GKE (~2-4 weeks)",
    "docker": "Containerize an existing project; Docker essentials course (~1 week)",
    "aws": "AWS Cloud Practitioner → Solutions Architect track (~4-6 weeks)",
    "terraform": "Infrastructure-as-code basics; provision a demo VPC (~1-2 weeks)",
    "pytorch": "Follow a practical deep-learning course and port one scikit-learn project (~2-3 weeks)",
    "tensorflow": "TensorFlow developer certificate track (~3-4 weeks)",
    "react": "Official React tutorial + one portfolio SPA (~2-3 weeks)",
    "node.js": "Build a REST API with Express + one SQL DB (~2 weeks)",
    "typescript": "Convert an existing JS project to TS (~1 week)",
    "sql": "Interactive SQL course + window functions (~1-2 weeks)",
    "power bi": "Microsoft PL-300 learning path (~2 weeks)",
    "tableau": "Tableau Public dashboards from open datasets (~1-2 weeks)",
    "mlops": "Package a model with CI + model registry (MLflow) (~2-3 weeks)",
    "llm": "Build a small RAG app with an open model API (~1-2 weeks)",
    "nlp": "Hugging Face NLP course (~2-3 weeks)",
    "spark": "PySpark on a 1M-row dataset (~2 weeks)",
    "ci/cd": "Set up GitHub Actions for an existing repo (~3-5 days)",
    "system design": "Grokking-style system design primer + mock designs (~4 weeks)",
    "microservices": "Split a monolith demo into 2-3 services with an API gateway (~3 weeks)",
    "statistics": "Refresh inference & hypothesis testing via a hands-on A/B project (~2 weeks)",
    "a/b testing": "Design and analyze one simulated experiment end-to-end (~1 week)",
    "excel": "Advanced formulas + pivot tables on a real dataset (~1 week)",
    "python": "Python for automation/data track + small projects (~3-4 weeks)",
    "selenium": "Automate one regression suite (~1-2 weeks)",
    "kafka": "Build a producer/consumer demo with one real use case (~2 weeks)",
    "flutter": "Ship one cross-platform demo app (~3 weeks)",
}

DEFAULT_HINT = "Pick a focused project-based course; add one proof-of-work artifact to the resume (~2-4 weeks)"


class SkillGapAgent:
    name = "Skill Gap Agent"
    description = "Turns missing requirements into prioritized gaps with adjacent strengths and upskilling recommendations."

    def analyze(self, profile, requirements, match_result):
        cand = profile.get("skills") or []
        cand_by_cat = {}
        for s in cand:
            if isinstance(s, dict):
                cand_by_cat.setdefault(s.get("category", "Other"), []).append(s["name"])

        critical = []
        for name in match_result.get("must_missing") or []:
            critical.append({"skill": name, "severity": "critical",
                             "recommendation": LEARNING_HINTS.get(name.lower(), DEFAULT_HINT)})

        stretch = []
        for name in match_result.get("nice_missing") or []:
            stretch.append({"skill": name, "severity": "nice-to-have",
                            "recommendation": LEARNING_HINTS.get(name.lower(), DEFAULT_HINT)})

        # Adjacent strengths: candidate skills in the same category as a critical gap
        adjacent = []
        seen = set()
        for gap in critical:
            cat = None
            for s in cand:
                if isinstance(s, dict):
                    from agents.matching_agent import skill_match
                    if skill_match(s["name"], gap["skill"]):
                        cat = s.get("category")
            # category of the missing skill itself (from requirements)
            for req in (requirements.get("must_have_skills") or []) + (requirements.get("nice_to_have_skills") or []):
                if req["name"].lower() == gap["skill"].lower():
                    cat = req.get("category") or cat
            if cat and cat in cand_by_cat:
                strengths = [n for n in cand_by_cat[cat] if n.lower() != gap["skill"].lower()][:3]
                if strengths:
                    key = (gap["skill"], tuple(strengths))
                    if key not in seen:
                        seen.add(key)
                        adjacent.append({"gap": gap["skill"], "category": cat, "build_on": strengths})

        coverage = match_result["components"]["must_have"]
        gap_score = 100 - coverage["score"]  # higher = larger gap in must-haves

        return {
            "gap_score": gap_score,
            "critical_gaps": critical,
            "stretch_gaps": stretch,
            "adjacent_strengths": adjacent[:5],
            "matched_count": coverage["matched"],
            "required_count": coverage["total"],
            "summary": (
                f"{coverage['matched']}/{coverage['total']} must-have skills covered"
                + (f"; {len(critical)} critical gap(s) to close" if critical else "; all must-have skills covered")
            ),
        }
