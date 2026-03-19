from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from cve_fetcher import get_cve_data
from suggestions import get_suggestion

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
        
        suggestion = get_suggestion(cve_info["cve_count"])
        
        cve_info["suggestion"] = suggestion
        
        results.append(cve_info)
    
    return {
        "dependencies": results
    }
def clean_dependencies(deps):
    return [d.strip().lower() for d in deps if d.strip()]