from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

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
    return {
        "received_dependencies": data.dependencies,
        "message": "Analysis will be implemented next"
    }