from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from cve_fetcher import get_cve_data
from github_analyzer import get_github_data
from predictor import get_ml_risk_analysis

app = FastAPI()
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
    return {"message": "Backend is running 🚀"}


@app.post("/analyze")
def analyze(data: DependencyInput):
    cleaned = clean_dependencies(data.dependencies)
    results = []
    for dep in cleaned:
        cve_info = get_cve_data(dep)
        github_info = get_github_data(dep)

        risk_score, status = get_ml_risk_analysis(
            cve_info["cve_count"],
            github_info["stars"],
            github_info["open_issues"],
            github_info["last_updated_days"]
        )

        results.append({
            "package": dep,
            "risk_score": risk_score,
            "status": status,
            "details": github_info
        })
    return {"dependencies": results}


def clean_dependencies(deps):
    return [d.strip().lower() for d in deps if d.strip()]
