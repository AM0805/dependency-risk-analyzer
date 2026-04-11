from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from cve_fetcher import get_cve_data
from github_analyzer import get_github_data
from predictor import get_ml_risk_analysis
from suggestions import get_alternatives

app = FastAPI()

# Enable CORS so your frontend can talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DependencyInput(BaseModel):
    dependencies: List[str]

@app.get("/")
def home():
    return {"message": "Dependency Risk Analyzer API is Live 🚀"}


@app.get("/alternatives/{package}")
def alternatives(package: str, original_score: int = 100):
    candidates = get_alternatives(package)
    results = []
    for alt in candidates:
        try:
            cve_info = get_cve_data(alt)
            github_info = get_github_data(alt)
            # Skip packages with no GitHub presence
            if github_info["stars"] == 0 and github_info["last_updated_days"] == 999:
                continue
            risk_score, status = get_ml_risk_analysis(
                cve_info["cve_count"], cve_info["avg_cvss"],
                github_info["stars"], github_info["open_issues"],
                github_info["last_updated_days"]
            )
            # Only include if strictly lower risk than the original
            if risk_score < original_score:
                results.append({"package": alt, "risk_score": risk_score, "status": status})
        except Exception:
            continue
    results.sort(key=lambda x: x["risk_score"])
    return {"alternatives": results}

@app.post("/analyze")
def analyze(data: DependencyInput):
    cleaned = [d.strip().lower() for d in data.dependencies if d.strip()]
    results = []
    
    for dep in cleaned:
        cve_info = get_cve_data(dep)
        github_info = get_github_data(dep)

        # Now passing all 5 features to the trained model
        risk_score, status = get_ml_risk_analysis(
            cve_info["cve_count"],
            cve_info["avg_cvss"],
            github_info["stars"],
            github_info["open_issues"],
            github_info["last_updated_days"]
        )

        results.append({
            "package": dep,
            "risk_score": risk_score,
            "status": status,
            "details": {
                "stars": github_info["stars"],
                "open_issues": github_info["open_issues"],
                "last_updated_days": github_info["last_updated_days"],
                "cve_count": cve_info["cve_count"],
                "avg_cvss": round(cve_info.get("avg_cvss", 0), 2)
            }
        })
        
    return {"dependencies": results}