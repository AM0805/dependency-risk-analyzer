from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from cve_fetcher import get_cve_data
from suggestions import get_suggestion
from github_analyzer import get_github_data

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

class DependencyInput(BaseModel):
    dependencies: List[str]

@app.post("/analyze")
def analyze(data: DependencyInput):
    
    cleaned = clean_dependencies(data.dependencies)
    
    results = []
    
    for dep in cleaned:
        
        cve_info = get_cve_data(dep)
        github_info = get_github_data(dep)
        
        suggestion = get_suggestion(
            cve_info["cve_count"],
            github_info["stars"],
            github_info["last_updated_days"]
        )
        
        combined = {
            "package": dep,
            "cve_count": cve_info["cve_count"],
            "stars": github_info["stars"],
            "open_issues": github_info["open_issues"],
            "last_updated_days": github_info["last_updated_days"],
            "suggestion": suggestion
        }
        
        results.append(combined)
    
    return {
        "dependencies": results
    }
    
    cleaned = clean_dependencies(data.dependencies)
    
    results = []
    
    for dep in cleaned:
        cve_info = get_cve_data(dep)
        
        suggestion = get_suggestion(cve_info["cve_count"])
        
        cve_info["suggestion"] = suggestion
        
        results.append(cve_info)
    
    return {
        "dependencies": results
    }
def clean_dependencies(deps):
    return [d.strip().lower() for d in deps if d.strip()]