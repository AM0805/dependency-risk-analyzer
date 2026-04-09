import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from pypi_fetcher import get_repo_url
from services.cache import get_from_cache, set_cache

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def extract_repo_name(url):
    if not url or "github.com" not in url:
        return None
    parts = url.split("github.com/")
    repo_part = parts[1].strip("/")
    repo_parts = repo_part.split("/")
    if len(repo_parts) < 2:
        return None
    return repo_parts[0] + "/" + repo_parts[1]

def get_github_data(package_name):
    key = f"github:{package_name}"
    cached = get_from_cache(key)
    if cached:
        return cached

    print(f"CACHE MISS: {key}")
    repo_url = get_repo_url(package_name)
    repo = extract_repo_name(repo_url)
    
    common_map = {
        "numpy": "numpy/numpy", "pandas": "pandas-dev/pandas",
        "django": "django/django", "flask": "pallets/flask",
        "requests": "psf/requests", "fastapi": "tiangolo/fastapi"
    }

    if not repo:
        repo = common_map.get(package_name)

    if not repo:
        result = {"stars": 0, "open_issues": 0, "last_updated_days": 999}
        set_cache(key, result)
        return result

    url = f"https://api.github.com/repos/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "dependency-risk-analyzer"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        result = {"stars": 0, "open_issues": 0, "last_updated_days": 999}
        set_cache(key, result)
        return result

    data = response.json()
    pushed_at_str = data.get("pushed_at")
    if pushed_at_str:
        pushed_at = datetime.fromisoformat(pushed_at_str.replace("Z", "+00:00"))
        last_updated_days = (datetime.now(timezone.utc) - pushed_at).days
    else:
        last_updated_days = 365

    result = {
        "stars": data.get("stargazers_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "last_updated_days": max(0, last_updated_days)
    }
    set_cache(key, result)
    return result